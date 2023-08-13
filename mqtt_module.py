import paho.mqtt.client as mqtt
from collector import *
import json

mqtt_server="central.local"
mqtt_port=1883

class mqttModule:
    def __init__(self):
        self._client =mqtt.Client()
        self._client.on_log=self._on_log
        self._client.on_message=self._on_message
        self._client.on_connect=self._on_connect
        self._client.on_disconnect=self._on_disconnect
        self._client.connect(mqtt_server, mqtt_port)
        self.on_connection_changes=self._on_connection_changes
        self._subscribtion=dict()
        self._client.loop_start()
        pass

    def _on_connection_changes(self,state):
        print("conection state= ",state)
        pass

    def _on_log(self,client, userdata, level, buf):
        print("log: ",buf)
        pass

    def _on_message(self,client, userdata, message):
        msg_dict=json.loads(message.payload.decode("utf-8"))
        print("message received  ",msg_dict, "topic",message.topic,"retained ",message.retain)
        if message.topic in self._subscribtion:
            self._subscribtion[message.topic](msg_dict)
        if message.retain==1:
            print("This is a retained message")
        pass
        
    def _on_connect(self, client, userdata, flags, rc):
        if rc==0:
            print("connected OK")
            for topic in self._subscribtion.keys():
                self._subscribe(topic)
            self.on_connection_changes(True)
        else:
            print("Bad connection Returned code=",rc)
        pass

    def _on_disconnect(self, client, userdata, rc):
        print("disconnecting reason  "  +str(rc))
        self.on_connection_changes(False)
#        self._client.connect(mqtt_server, mqtt_port)
        pass

    def _subscribe(self,topic):
        if  self._client.is_connected():
            print("mqtt subscribe topic ",topic);
            self._client.subscribe(topic)
            pass
        pass

    def subscribe(self,topic, cb_function):
        self._subscribtion[topic]=cb_function
        if  self._client.is_connected():
            self._subscribe(topic)
            pass
        pass

class CObjCommon:
    object_id=0
    def __init__(self,name,topic):
        CObjCommon.object_id += 1
        self._data = {}
        self._data["name"]=name
        self._data["topic"] = topic
        self._data["id"] = CObjCommon.object_id
        pass
    def get_name(self):
        return self._data["name"]
    def get_topic(self):
        return self._data["topic"]
    def get_data(self):
        return self._data
    def get_id(self):
        return self._data["id"]
    pass

class CWeather(CObjCommon):
    def __init__(self,name,topic):
        super().__init__(name,topic)
        pass

    def on_message(self,msg):
        if "bmp180" in msg:
            add_value_dict(self._data, "pressure", msg["bmp180"], "pressure", 7 * 24 * 60 * 60)
            pass
        if "dht" in msg:
            set_value(self._data, "humidity", msg["dht"], "humidity")
            add_value_dict(self._data, "temperature", msg["dht"], "temperature", 7 * 24 * 60 * 60)
            pass
        if "battery" in msg:
            set_value(self._data, "battery", msg["battery"], "value")
            pass
        if "BH1750" in msg:
            set_value(self._data, "lighting", msg["BH1750"], "value")
            pass
        if "wifi" in msg:
            set_value(self._data, "rssi", msg["wifi"], "rssi")
            pass
        pass
    pass

class CClock(CObjCommon):
    def __init__(self,name,topic):
        super().__init__(name,topic)
        pass

    def on_message(self,msg):
        set_value(self._data, "temperature", msg, "temperature")
        set_value(self._data, "humidity", msg, "humidity")
        set_value(self._data, "rssi", msg, "rssi")
        print(msg)
        pass
    pass