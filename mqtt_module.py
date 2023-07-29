import paho.mqtt.client as mqtt
import time
import json

mqtt_server="central.local"
mqtt_port=1883

class mqttModule:
    def __init__(self):
        self._client =mqtt.Client("central")
        self._client.on_log=self._on_log
        self._client.on_message=self._on_message
        self._client.on_connect=self._on_connect
        self._client.on_disconnect=self._on_disconnect
        self._client.connect(mqtt_server, mqtt_port)
        self.on_connection_changes=self._on_connection_changes
        self._subscribtion=dict()
        pass

    def _on_connection_changes(self,state):
        print("conection state= ",state)
        pass

    def _on_log(self,client, userdata, level, buf):
        print("log: ",buf)
        pass

    def _on_message(self,client, userdata, message):
        msg_json=json.loads(message.payload.decode("utf-8"))
        print("message received  ",msg_json, "topic",message.topic,"retained ",message.retain)
        self._subscribtion[message.topic](msg_json)
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
        self._client.connect(mqtt_server, mqtt_port)
        pass

    def loop(self):
        self._client.loop()
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
