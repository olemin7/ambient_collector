import json
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from threading import Lock
from mqtt_module import mqttModule
from obj_mqtt import CWeather,CClock
from functools import partial

mqtt_module=mqttModule()

app = Flask(__name__)
app.config["SECRET_KEY"] = "asfdwe"
socketio = SocketIO(app, cors_allowed_origins="*")

weather =CWeather("Вулиця","stat/weather","update_weather")
rooms_data=[CClock("Батьки","stat/clock_parent","update_weather"),
       CClock("Діти","stat/clock_children","update_weather"),
       CClock("майстерня","stat/clock_workshop","update_weather")]

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

def mqtt_handler(handler,msg):
    handler.on_message(msg)
    as_json = json_dumps_fround(handler.get_data())
    socketio.emit(handler.get_event(), as_json)
    pass

def start():
    mqtt_module.subscribe(weather.get_topic(),partial(mqtt_handler,weather))
    for el in rooms_data:
        mqtt_module.subscribe(el.get_topic(), partial(mqtt_handler, el))
        pass
    pass

"""
Serve root index file
"""

@app.route("/")
@app.route("/outdoors")
def outdoors():
    return render_template("outdoors.html")

@app.route("/rooms")
def rooms():
    return render_template("rooms.html",rooms=rooms_data)

"""
Decorator for connect
"""

@socketio.on("connect")
def connect():
    print("Client connected")
    update={'weather':weather.get_data()}
    update_json = json_dumps_fround(update)
    socketio.emit("update", update_json)
    pass


"""
Decorator for disconnect
"""


@socketio.on("disconnect")
def disconnect():
    print("Client disconnected", request.sid)

start()
#if __name__ == "__main__":
#    socketio.run(app, port=5000, host="0.0.0.0", debug=True)
