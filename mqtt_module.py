import paho.mqtt.client as mqtt
import json
import logging
from collections.abc import Callable
import config
import transformation
import pytest

log = logging.getLogger('logger')

class MQTTModule:
    def __init__(self, host: str, port: int, topics: set, on_msg_cb: Callable[[str, str], None]):
        self._client = mqtt.Client()
        self._client.on_log = self._on_log
        self._client.on_message = self._on_message
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self.__on_msg_cb = on_msg_cb
        self._subscription = topics
        log.debug(f"topics: {topics}")
        self._client.connect(host, port)
        self._client.loop_start()

    def _on_log(self, client, userdata, level, buf):
        log.info(f"log: {buf}")

    def _on_message(self, client, userdata, message):
        msg = message.payload.decode("utf-8")
        log.info(f"message received , topic={message.topic} : {msg} , retained {message.retain}")
        self.__on_msg_cb(message.topic, msg)

        if message.retain == 1:
            log.info("This is a retained message")
        pass

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            log.info("connected OK")
            for topic in self._subscription:
                self._client.subscribe(topic)
        else:
            log.info("Bad connection Returned code=", rc)

    def _on_disconnect(self, client, userdata, rc):
        log.info(f"disconnecting reason {str(rc)}")


class MQTTThings(MQTTModule):
    def __init__(self, config_mqtt:dict, config_things:[], on_data_cb: Callable[[str,object], None]):
        self.__on_data_cb_cb = on_data_cb
        self.__things=config_things
        topics=set()
        for thing in self.__things:
            if "parameters" in thing:
                for parameter in thing["parameters"]:
                    topics.add(parameter["topic"])
        super().__init__(config_mqtt["server"], config_mqtt["port"], topics, self.__on_message)

    @staticmethod
    def parse_field(payload:str,parameter:dict)->object:
        if "field" in parameter:
            json_obj = json.loads(payload)  # to do inner json outer.inner....field
            for field in parameter["field"].split('.'):
                if (type(json_obj) is  dict)and  (field in json_obj):
                    json_obj=json_obj[field]
                else:
                    return None
            return json_obj
        else:
           return payload

    def __on_message(self, topic: str, payload: str):
        for thing in self.__things:
            if "parameters" in thing:
                for parameter in thing["parameters"]:
                    if topic == parameter["topic"]:
                        value=MQTTThings.parse_field(payload,parameter)
                        if value is not None:
                            if "type" in parameter:
                                value =transformation.to_type(value,parameter["type"])
                            self.__on_data_cb_cb(config.get_parameter_name(thing["name"], parameter), value)
        pass

class MQTTAdvertisement(MQTTModule):
    TOPIC_ADVERTISEMENT = "advertisement"
    TOPIC_CMD = "cmd"
    CMD_ADVERTISEMENT = "adv"

    def __init__(self, config_mqtt: dict, config_things:[], on_data_cb: Callable[[str, object], None]):
        self.__on_data_cb_cb = on_data_cb
        self.__known_thing_by_mac=dict()
        for thing in config_things:
            if "mac" in thing and "name" in thing:
                self.__known_thing_by_mac[thing["mac"]]=thing["name"]
        super().__init__(config_mqtt["server"], config_mqtt["port"], [MQTTAdvertisement.TOPIC_ADVERTISEMENT], self.__on_message)

    def _on_connect(self, client, userdata, flags, rc):
        super()._on_connect(client, userdata, flags, rc)
        log.debug(r"send advertisement")
        self._client.publish(MQTTAdvertisement.TOPIC_CMD, MQTTAdvertisement.CMD_ADVERTISEMENT)

    def __on_message(self, topic: str, payload: str):
        json_obj = json.loads(payload)
        mac=json_obj["mac"]
        if mac in self.__known_thing_by_mac:
            json_obj["name"]=self.__known_thing_by_mac[mac]
        self.__on_data_cb_cb(f"{MQTTAdvertisement.TOPIC_ADVERTISEMENT}.{mac}", json_obj)



@pytest.mark.parametrize("payload,parameter,result", [("10", {},"10"),
                                                      ("10", {'field':"f0"},None),
                                                      ('{"f0":10}', {'field':"f0"},10),
                                                      ('{"f0":{"f1":10}}', {'field':"f0.f1"},10),
                                                      ('{"f0":{"f1":10}}', {'field':"f0.f3"},None),
                                                        ('{"f0":{"f1":10}}', {'field':"f0.f1.f3"},None),
                                                      ])
def test_parse_field(payload,parameter,result):
    assert MQTTThings.parse_field(payload,parameter)==result

