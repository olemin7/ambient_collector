import json
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from mqtt_module import MQTTThings,MQTTAdvertisement
#from alive_tracker import *
from datetime import datetime, timezone
import config
import map_tree
import collector
from tbot_module import TBot, tbot_send_https_notice
import asyncio
import threading
import logging
import transformation
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
config_inst = config.get("config/config.yaml")
collector_inst =collector.COLLECTOR(config_inst)
mqtt_things= None
mqtt_advertisement= None
tBot = TBot()
app = Flask(__name__)
app.config["SECRET_KEY"] = "asfdwe"
socketio = SocketIO(app, cors_allowed_origins="*")
event_loop = asyncio.new_event_loop()
asyncio.set_event_loop(event_loop)

def on_thing_event(name:str,value:object):
    log.debug(f"MQTTThings {name}={value}")
    current_data.set(name,value)
    collector_inst.set(name, value) # store to DB
    socketio.emit("event",{"name":name, "value":value}) #to frontend





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
        config_inst['telegram'] = cfg
        yaml.dump(config_inst, file)
        log.info(f"config_updated={config_inst}")


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
        tbot_send_https_notice(config_inst['telegram'], status)


def socketio_background_thread():
    while True:
        # log.debug("background_thread")
        # power220tracker.refresh()
        socketio.sleep(5)


def start():
    collector_inst.prune()
    mqtt_things = MQTTThings(config_inst["mqtt"], config_inst["things"], on_thing_event)
    mqtt_advertisement = MQTTAdvertisement(config_inst["mqtt"], on_thing_event)
    for key in collector_inst.get_available_fields():
        ts,val=collector_inst.get_tail(key)
     #   current_data.set(key,val)
        log.info(f"last state [{datetime.fromtimestamp(ts, timezone.utc)}]{key}:{val}")

    # for el in things:
    #     el.on_update(lambda data: socketio.emit("thing", data))
    # power220tracker.on_change(on_power220_update)


    def tbot_thread(loop):
        asyncio.set_event_loop(loop)
        asyncio.run(tBot.start(config_inst["telegram"]))

    threading.Thread(target=tbot_thread, name='telebot', args=(event_loop,)).start()
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(socketio_background_thread)


"""
Serve root index file
"""
@socketio.on("history" )
def got_cmd(arg):
    tmp=collector_inst.get_range(arg["key"],arg["begin"] if "begin" in arg else None,arg["end"] if "end" in arg else None)
    if "transformation" in arg:
        param=arg["transformation"]
        param["to_type"]="float2"
        tmp=transformation.tranformation(tmp,param)
    log.debug(tmp)
    return tmp

@app.route("/")
@app.route("/outdoors")
def outdoors_page():
    summary = [("Температура", "parent.temperature"),
               ("Батарея", "battery")]
    graphs = ["id_comp_outdoor.temperature", "id_comp_outdoor.light", "id_h_outdoor.temperature", "id_h_presure", "id_h_light"]
    return render_template("outdoors.html", summary=summary, graphs=graphs)


@app.route("/rooms")
def rooms_page():
    rooms = []
    for el in config_inst["things"]:
        if "room" in el["property"]:
            rooms.append(el)
    log.debug(f"rooms {rooms}")
    return render_template("rooms.html", rooms=rooms)


@app.route("/power220")
def psu_page():
    return render_template("power220.html")


@app.route("/things")
def things_page():
    return render_template("things.html")


"""
Decorator for connect
"""


@socketio.on("connect")
def connect():
    print("Client connected")
    socketio.emit("current_data", current_data.get())


"""
Decorator for disconnect
"""


@socketio.on("disconnect")
def disconnect():
    print("Client disconnected", request.sid)


start()

# if __name__ == "__main__":
#    socketio.run(app, port=5000, host="0.0.0.0", debug=True)
