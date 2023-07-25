import json
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from random import random
from threading import Lock
from datetime import datetime
from mqtt_module import mqttModule
import board


mqtt_module=mqttModule()

thread = None
thread_lock = Lock()

app = Flask(__name__)
app.config["SECRET_KEY"] = "asfdwe"
socketio = SocketIO(app, cors_allowed_origins="*")



def topic_weather(msg_json):
    upd={}
    upd["temperature"]=msg_json["dht"]["temperature"]
    upd["humidity"]=msg_json["dht"]["humidity"]
    upd["pressure"]=msg_json["bmp180"]["pressure"]
    upd["battery"]=3
    upd["lighting"]=3
    upd["rssi"]=-49

    sensor_json = json.dumps(upd)

    socketio.emit("weatherData", sensor_json)
    pass

mqtt_module.subscribe("stat/weather",topic_weather)

"""
Background Thread
"""


def background_thread():
    while True:
        mqtt_module.loop()
        socketio.sleep(3)


"""
Serve root index file
"""


@app.route("/")
def index():
    return render_template("index.html")


"""
Decorator for connect
"""


@socketio.on("connect")
def connect():
    global thread
    print("Client connected")
    socketio.emit("wholeData", {})

    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)


"""
Decorator for disconnect
"""


@socketio.on("disconnect")
def disconnect():
    print("Client disconnected", request.sid)



# if __name__ == "__main__":
#     socketio.run(app, port=5000, host="0.0.0.0", debug=True)
