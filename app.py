import json
import os
import yaml
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from mqtt_module import MQTTThings, MQTTAdvertisement
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
import engineio.payload

# The client fires many "history" emits at page load; while still on HTTP
# long-polling, engine.io batches them into one POST. The default limit of 16
# packets/payload raises "Too many packets in payload". Raise it for this app.
engineio.payload.Payload.max_decode_packets = 250

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
CONFIG_FILE = "config/config.yaml"
config_inst = config.get(CONFIG_FILE)
collector_inst = collector.Collector(config_inst)
mqtt_things = None
mqtt_advertisement = None
tBot = TBot()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-fallback-key")
socketio = SocketIO(app, cors_allowed_origins="*")

def on_thing_event(name:str,value:object):
    log.debug(f"MQTTThings {name}={value}")
    current_data.set(name,value)
    collector_inst.set(name, value) # store to DB
    socketio.emit("event",{"name":name, "value":value}) #to frontend



@tBot.set_get_status_fn
def status():
    #for debug
    # cur_weather = getLastElement(weather.get_data()["collector"], 'temperature')
    # log.debug(f"weather={cur_weather}")
    # status = ""
    # if (cur_weather):
    #     status += f"Вулиця ={round(cur_weather['temperature'], 1)}ºC"
    # if "state" in power220tracker.get_data():
    #     result += f"\nмережа {power220tracker.get_data()['state']}"
    result = ""
    log.info(f"send status={result}")
    return result


@tBot.set_config_updated_cb
def config_updated(cfg):
    # Persist ONLY the telegram section, preserving the original (unexpanded)
    # config file structure. Dumping the in-memory config_inst would inline all
    # the per-thing parameters that were loaded from separate files and clobber
    # config.yaml. Re-read the raw file and swap just the telegram block.
    with open(CONFIG_FILE) as file:
        raw_config = yaml.safe_load(file)
    telegram_to_save = dict(cfg)
    subscribers = telegram_to_save.get('subscribers')
    if isinstance(subscribers, set):
        telegram_to_save['subscribers'] = sorted(subscribers)
    raw_config['telegram'] = telegram_to_save
    with open(CONFIG_FILE, 'w') as file:
        yaml.safe_dump(raw_config, file, sort_keys=False, allow_unicode=True)
    log.info(f"config_updated telegram={telegram_to_save}")


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
    global thread, mqtt_things, mqtt_advertisement
    # Guard against running more than once per process (e.g. Flask reloader,
    # repeated imports). Telegram polling in particular must be single-instance.
    with thread_lock:
        if thread is not None:
            log.info("start() already initialized; skipping")
            return
        thread = socketio.start_background_task(socketio_background_thread)

    collector_inst.prune()
    mqtt_things = MQTTThings(config_inst["mqtt"], config_inst["things"], on_thing_event)
    mqtt_advertisement = MQTTAdvertisement(config_inst["mqtt"], config_inst["things"], on_thing_event)
    for key in collector_inst.get_available_fields():
        ts, val = collector_inst.get_tail(key)
        log.info(f"last state [{datetime.fromtimestamp(ts, timezone.utc)}]{key}:{val}")
        current_data.set(key, val)

    def tbot_thread():
        # asyncio.run creates and owns its own event loop for this thread.
        asyncio.run(tBot.start(config_inst["telegram"]))

    threading.Thread(target=tbot_thread, name='telebot', daemon=True).start()


@socketio.on("history")
def got_cmd(arg):
    tmp = collector_inst.get_range(arg["key"], arg.get("begin"), arg.get("end"))
    if "transformation" in arg:
        param = arg["transformation"]
        param["to_type"] = "float2"
        tmp = transformation.transformation(tmp, param)
    log.debug(tmp)
    return tmp

@app.route("/")
@app.route("/outdoors")
def outdoors_page():
    summary = [("Температура", "outdoor.temperature"),
               ("Батарея", "outdoor.battery")]
    graphs = ["id_comp_outdoor.temperature", "id_comp_outdoor.light", "id_min_max_outdoor.temperature", "id_h_outdoor.pressure", "id_h_light"]
    return render_template("outdoors.html", summary=summary, graphs=graphs)


@app.route("/rooms")
def rooms_page():
    rooms = []
    for el in config_inst["things"]:
        if "room" in el["property"]:
            rooms.append(el["name"])
    log.debug(f"rooms {rooms}")
    graphs = ["temperature"]
    return render_template("rooms.html", rooms=rooms, graphs=graphs)


@app.route("/power220")
def psu_page():
    return render_template("power220.html")


@app.route("/things")
def things_page():
    return render_template("things.html")


@socketio.on("connect")
def connect():
    log.debug("Client connected")
    socketio.emit("current_data", current_data.get())


@socketio.on("disconnect")
def disconnect():
    log.debug(f"Client disconnected {request.sid}")


start()
