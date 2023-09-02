import json
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from mqtt_module import mqttModule, CWeather, CClock
try:
    from gpio_module import CGPIOpsu
    psu = CGPIOpsu()
except (ImportError, RuntimeError):
    pass
from tbot_module import TBot
from functools import partial
import yaml

config={}
mqtt_module=mqttModule()

app = Flask(__name__)
app.config["SECRET_KEY"] = "asfdwe"
socketio = SocketIO(app, cors_allowed_origins="*")

weather =CWeather("Вулиця","sensors/weather")
rooms_data=[CClock("Батьки","stat/clock_parent"),
       CClock("Діти","stat/clock_children"),
       CClock("Майстерня","stat/clock_workshop")]


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

def psu_state_update(state):
    socketio.emit('update_psu', state)

def mqtt_handler_wrapper(handler,event,msg):
    handler.on_message(msg)
    socketio.emit(event, handler.get_data())

def start():
    with open("config.yaml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    print('config=',config)
    mqtt_module.subscribe(weather.get_topic(),partial(mqtt_handler_wrapper,weather,"update_weather"))
    for el in rooms_data:
        mqtt_module.subscribe(el.get_topic(), partial(mqtt_handler_wrapper, el,"update_room"))
    if 'psu' in globals():
        psu.set_cb(psu_state_update)

"""
Serve root index file
"""

@app.route("/")
@app.route("/outdoors")
def outdoors_page():
    return render_template("outdoors.html")

@app.route("/rooms")
def rooms_page():
    return render_template("rooms.html",rooms=rooms_data)

@app.route("/psu")
def psu_page():
    return render_template("psu.html")

"""
Decorator for connect
"""

@socketio.on("connect")
def connect():
    print("Client connected")
    update={'weather':weather.get_data(),'rooms':[]}
    if 'psu' in globals():
        update['psu']=psu.get_data()

    for el in rooms_data:
        update["rooms"].append(el.get_data())
    socketio.emit("update", update)


"""
Decorator for disconnect
"""


@socketio.on("disconnect")
def disconnect():
    print("Client disconnected", request.sid)

start()
#if __name__ == "__main__":
#    socketio.run(app, port=5000, host="0.0.0.0", debug=True)
