import json
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from mqtt_module import MQTTThings,MQTTAdvertisement
from collector import *
#from alive_tracker import *
import config
import map_tree
from tbot_module import TBot, tbot_send_https_notice
import asyncio
import threading
import logging
from systemd import journal
from threading import Lock

logging.basicConfig(format=' %(levelname)s %(asctime)s:%(filename)s:%(lineno)d: %(message)s', level=logging.DEBUG)
log = logging.getLogger('logger')
thread = None
thread_lock = Lock()
current_data= map_tree.MapTree()

try:
    log.addHandler(journal.JournalHandler())
except (ImportError, RuntimeError, AttributeError):
    log.addHandler(journal.JournaldLogHandler())

log.setLevel(logging.DEBUG)
config = config.get("config/config.yaml")

tBot = TBot()
app = Flask(__name__)
app.config["SECRET_KEY"] = "asfdwe"
socketio = SocketIO(app, cors_allowed_origins="*")
event_loop = asyncio.new_event_loop()
asyncio.set_event_loop(event_loop)

def on_thing_event(name:str,event:object):
    log.debug(f"MQTTThings {name}={event}")
    current_data.set(name,event)
    socketio.emit(name, event) #to frontend
    # add store to DB

mqtt_things= MQTTThings(config["mqtt"],config["things"],on_thing_event)
mqtt_advertisement= MQTTAdvertisement(config["mqtt"],on_thing_event)



# weather = CWeather("Вулиця", "sensors/weather", ["weather"], config)
# power220tracker = CAliveTracker("Живлення220", "stat/power", ["power220"], config)
# things=[]
# things = [weather,
#           CClock("Батьківська", "stat/clock_parent", ["room"], config),
#           CClock("Дитяча", "stat/clock_children", ["room"], config),
#           CClock("Майстерня", "stat/clock_workshop", ["room"], config),
#           CClock("Коридор", "stat/clock_hall", ["room"], config),
#           power220tracker
#           ]


@tBot.set_get_status_fn
def status():
    # cur_weather = getLastElement(weather.get_data()["collector"], 'temperature')
    # log.debug(f"weather={cur_weather}")
    # status = ""
    # if (cur_weather):
    #     status += f"Вулиця ={round(cur_weather['temperature'], 1)}ºC"
    # if "state" in power220tracker.get_data():
    #     status += f"\nмережа {power220tracker.get_data()['state']}"
    log.info(f"send status={status}")
    return status


@tBot.set_config_updated_cb
def config_updated(cfg):
    with open(config_file, 'w') as file:
        config['telegram'] = cfg
        yaml.dump(config, file)
        log.info(f"config_updated={config}")


def json_dumps_fround(field):
    def json_round_floats(o):
        if isinstance(o, float):
            return round(o, 3)
        if isinstance(o, dict):
            return {k: json_round_floats(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [json_round_floats(x) for x in o]
        return o

    return json.dumps(json_round_floats(field))


def on_power220_update(data):
    if "state" in data:
        status = f"живлення {data['state']}"
        tbot_send_https_notice(config['telegram'], status)


def socketio_background_thread():
    while True:
        # log.debug("background_thread")
        # power220tracker.refresh()
        socketio.sleep(5)


def start():
    # mqtt_module.start(config["mqtt"],config["things"])
    # for el in things:
    #     el.on_update(lambda data: socketio.emit("thing", data))
    # power220tracker.on_change(on_power220_update)

    # mqtt_module.subscribe("advertisement", el.on_message){
    #
    # }

    def tbot_thread(loop):
        asyncio.set_event_loop(loop)
        asyncio.run(tBot.start(config["telegram"]))

    threading.Thread(target=tbot_thread, name='telebot', args=(event_loop,)).start()
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(socketio_background_thread)


"""
Serve root index file
"""


@app.route("/")
@app.route("/outdoors")
def outdoors_page():
    summary = [("Температура", "temperature"),
               ("Батарея", "battery")]
    graphs = ["id_h_temperature_cmp", "id_h_light_cmp", "id_h_temperature", "id_h_presure", "id_h_light"]
    return render_template("outdoors.html", summary=summary, graphs=graphs)


@app.route("/rooms")
def rooms_page():
    rooms = []
    for el in things:
        if "room" in el.get_masks():
            rooms.append(el)
    return render_template("rooms.html", rooms=rooms)


@app.route("/power220")
def psu_page():
    return render_template("power220.html")


@app.route("/things")
def things_page():
    return render_template("things.html", things=things)


"""
Decorator for connect
"""


@socketio.on("connect")
def connect():
    print("Client connected")
    update = {'things': []}
    # for el in things:
    #     update["things"].append(el.get_data())
    socketio.emit("update", update)


"""
Decorator for disconnect
"""


@socketio.on("disconnect")
def disconnect():
    print("Client disconnected", request.sid)


start()

# if __name__ == "__main__":
#    socketio.run(app, port=5000, host="0.0.0.0", debug=True)
