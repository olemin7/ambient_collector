import paho.mqtt.client as mqtt
from collector import *
import json
import logging
from thing import CThing

log= logging.getLogger('logger')

class mqttModule:
    def __init__(self):
        self._client =mqtt.Client()
        self._client.on_log=self._on_log
        self._client.on_message=self._on_message
        self._client.on_connect=self._on_connect
        self._client.on_disconnect=self._on_disconnect
        self.on_connection_changes=self._on_connection_changes
        self._subscribtion=dict()
        pass

    def start(self, config):
        self._client.connect(config["server"], config["port"])
        self._client.loop_start()

    def _on_connection_changes(self,state):
        log.info(f"conection state= {state}")
        pass

    def _on_log(self,client, userdata, level, buf):
        log.info(f"log: {buf}")
        pass

    def _on_message(self,client, userdata, message):
        msg_dict=json.loads(message.payload.decode("utf-8"))
        log.info(f"message received  {msg_dict}, topic={message.topic}, retained {message.retain}")
        if message.topic in self._subscribtion:
            self._subscribtion[message.topic](msg_dict)
        if message.retain==1:
            log.info("This is a retained message")
        pass
        
    def _on_connect(self, client, userdata, flags, rc):
        if rc==0:
            log.info("connected OK")
            for topic in self._subscribtion.keys():
                self._subscribe(topic)
            self.on_connection_changes(True)
        else:
            log.info("Bad connection Returned code=",rc)
        pass

    def _on_disconnect(self, client, userdata, rc):
        log.info(f"disconnecting reason { str(rc)}")
        self.on_connection_changes(False)
        pass

    def _subscribe(self,topic):
        if  self._client.is_connected():
            log.info(f"mqtt subscribe topic {topic}");
            self._client.subscribe(topic)
            pass
        pass

    def subscribe(self,topic, cb_function):
        self._subscribtion[topic]=cb_function
        if  self._client.is_connected():
            self._subscribe(topic)
            pass
        pass

class CWiFi(CThing):
    def __init__(self, name, topic, masks:set):
        super().__init__(name, topic, masks)
        pass

    def on_message(self, msg):
        set_value(self._data, "wifi", msg, "wifi")
        set_if_present(self._data, "mqtt_period", msg, "mqtt_period")

class CWeather(CWiFi):
    def __init__(self,name,topic, masks:set):
        super().__init__(name,topic,masks)
        pass

    def on_message(self,msg):
        super().on_message(msg)
        if "weather" in msg:
            add_value_dict(self._data, "pressure", msg["weather"], "pressure", 7 * 24 * 60 * 60)
            set_value(self._data, "humidity", msg["weather"], "humidity")
            add_value_dict(self._data, "temperature", msg["weather"], "temperature", 7 * 24 * 60 * 60)
            set_value(self._data, "ambient_light", msg["weather"], "ambient_light")
        set_value(self._data, "battery", msg, "battery")

class CClock(CWiFi):
    def __init__(self,name,topic,masks:set):
        super().__init__(name,topic,masks)

    def on_message(self,msg):
        super().on_message(msg)
        set_value(self._data, "temperature", msg, "temperature")
        set_value(self._data, "humidity", msg, "humidity")

