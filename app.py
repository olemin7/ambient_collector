import json
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from threading import Lock
from mqtt_module import mqttModule
from collector import *

mqtt_module=mqttModule()

thread = None
thread_lock = Lock()

app = Flask(__name__)
app.config["SECRET_KEY"] = "asfdwe"
socketio = SocketIO(app, cors_allowed_origins="*")

data_keeper=dict()
history_keeper=dict()

def topic_weather(msg):
    if "weather" not in data_keeper:
        data_keeper["weather"]=dict()
        pass
    if "bmp180" in msg:
        update_helper(data_keeper["weather"], msg["bmp180"], "pressure")
        update_history(history_keeper, "pressure", msg["bmp180"], "pressure", 7 * 24 * 60 * 60)
        data_keeper["weather"]['history_pressure'] = history_pack(history_keeper, 'temperature', 7 * 24 * 60 * 60,
                                                                     60 * 60)
        pass
    if "dht" in msg:
        update_helper(data_keeper["weather"], msg["dht"], "temperature")
        update_helper(data_keeper["weather"], msg["dht"], "humidity")
        update_history(history_keeper,"temperature", msg["dht"], "temperature",2*24*60*60)
        data_keeper["weather"]['history_temperature']=history_pack(history_keeper,'temperature',2*24*60*60,60*60)
        pass
    if "battery" in msg:
        update_helper4(data_keeper["weather"],"battery", msg["battery"], "value")
        pass
    if "BH1750" in msg:
        update_helper4(data_keeper["weather"],"lighting", msg["BH1750"], "value")
        pass
    if "wifi" in msg:
        update_helper(data_keeper["weather"], msg["wifi"], "rssi")
        pass
    sensor_json = json.dumps(data_keeper["weather"])
    socketio.emit("update_weather", sensor_json)
    pass

mqtt_module.subscribe("stat/weather",topic_weather)

"""
Background Thread
"""


def background_thread():
    while True:
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
    sensor_json = json.dumps(data_keeper)
    socketio.emit("update", sensor_json)
 
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)


"""
Decorator for disconnect
"""


@socketio.on("disconnect")
def disconnect():
    print("Client disconnected", request.sid)

#if __name__ == "__main__":
#    socketio.run(app, port=5000, host="0.0.0.0", debug=True)
