import paho.mqtt.client as mqtt
from collector import *
import json
import logging
from thing import CCollectorThing

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

class CMQTTThing(CCollectorThing):
    def __init__(self, name, topic:str, masks:set,config:dict):
        super().__init__(name, config["persistance_dir"])
        self.add_masks({"mqtt"})
        self.add_masks(masks)
        self._data["topic"] = topic


    def get_topic(self):
        return self._data["topic"]

    def _on_message(self, msg):
        set_if_present(self._data, "wifi", msg)
        set_if_present(self._data, "upd_period", msg)

    def on_message(self, msg):
        self._on_message(msg)
        self._update()

class CWeather(CMQTTThing):
    def __init__(self,name,topic, masks:set,config:dict):
        super().__init__(name,topic,masks,config)
        self._collector.add_field( {"temperature", "humidity","pressure","ambient_light","battery"})
        self._collector.set_period(24*30)
        self._collector.finalise()

    def _on_message(self,msg):
        super()._on_message(msg)
        if "weather" in msg:
            weather=msg["weather"]
            set_if_present(self._collector_tmp, "pressure", weather)
            set_if_present(self._collector_tmp, "humidity", weather)
            set_if_present(self._collector_tmp, "temperature", weather)
            set_if_present(self._collector_tmp, "ambient_light", weather)
        set_if_present(self._collector_tmp, "battery", msg)

class CClock(CMQTTThing):
    def __init__(self,name,topic,masks:set,config:dict):
        super().__init__(name,topic,masks,config)
        self._collector.add_field( {"temperature","humidity"})
        self._collector.set_period(24*2)
        self._collector.finalise()

    def _on_message(self,msg):
        super()._on_message(msg)
        set_if_present(self._collector_tmp, "humidity", msg)
        set_if_present(self._collector_tmp, "temperature", msg)


