import paho.mqtt.client as mqtt
import json
import logging
from collections.abc import Callable
import config

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

    def __on_message(self, topic: str, payload: str):
        for thing in self.__things:
            if "parameters" in thing:
                for parameter in thing["parameters"]:
                    if topic == parameter["topic"]:
                        value=None
                        if "payload_type" in parameter:
                            payload_type=parameter["payload_type"]
                            json_obj = json.loads(payload)
                            if "field" in parameter:
                                field=parameter["field"]
                                if field in json_obj:
                                    value= json_obj[field]
                            else:
                                value=json_obj
                        else:
                            value=payload
                        if value !=None:
                            if "type" in parameter:
                                data_type=parameter["type"]
                                if data_type=="float2":
                                    value=round(float(value),2)
                                elif data_type == "int":
                                    value = int(value)

                            self.__on_data_cb_cb(config.get_parameter_name(thing["name"], parameter), value)
        pass

class MQTTAdvertisement(MQTTModule):
    TOPIC_ADVERTISEMENT = "advertisement"
    TOPIC_CMD = "cmd"
    CMD_ADVERTISEMENT = "adv"

    def __init__(self, config_mqtt: dict, on_data_cb: Callable[[str, object], None]):
        self.__on_data_cb_cb = on_data_cb
        super().__init__(config_mqtt["server"], config_mqtt["port"], [MQTTAdvertisement.TOPIC_ADVERTISEMENT], self.__on_message)

    def _on_connect(self, client, userdata, flags, rc):
        super()._on_connect(client, userdata, flags, rc)
        log.debug(r"send advertisement")
        self._client.publish(MQTTAdvertisement.TOPIC_CMD, MQTTAdvertisement.CMD_ADVERTISEMENT)

    def __on_message(self, topic: str, payload: str):
        json_obj = json.loads(payload)
        self.__on_data_cb_cb(f"{MQTTAdvertisement.TOPIC_ADVERTISEMENT}.{json_obj["mac"]}", payload)