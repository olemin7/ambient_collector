import paho.mqtt.client as mqtt
from typing_extensions import overload

from collector import *
import json
import logging
from thing import CCollectorThing
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


class MQTTAdvertisement(MQTTModule):
    TOPIC_ADVERTISEMENT = "advertisement"
    TOPIC_CMD = "cmd"
    CMD_ADVERTISEMENT = "adv"

    def __init__(self, config_mqtt:dict, on_adv_cb: Callable[[object], None]):
        self.__on_advertisement_cb = on_adv_cb

        super().__init__(config_mqtt["server"], config_mqtt["port"], {MQTTAdvertisement.TOPIC_ADVERTISEMENT}, self.__on_advertisement)

    def __on_advertisement(self, topic: str, payload: str):
        adv = json.loads(payload)
        log.debug(f"advertisement{adv}")
        self.__on_advertisement_cb(adv)

    def _on_connect(self, client, userdata, flags, rc):
        super()._on_connect(client, userdata, flags, rc)
        log.debug(r"send advertisement")
        self._client.publish(MQTTAdvertisement.TOPIC_CMD, MQTTAdvertisement.CMD_ADVERTISEMENT)


class MQTTThings(MQTTModule):
    def __init__(self, config_mqtt:dict, config_things:[], on_data_cb: Callable[[str,str], None]):
        self.__on_data_cb_cb = on_data_cb
        self.__things=config_things
        topics=set()
        for thing in self.__things:
            for parameter in thing["parameters"]:
                topics.add(parameter["topic"])
        super().__init__(config_mqtt["server"], config_mqtt["port"], topics, self.__on_message)

    def __on_message(self, topic: str, payload: str):
        for thing in self.__things:
            for parameter in thing["parameters"]:
                if topic == parameter["topic"]:
                    value=None
                    if "jsonField" in parameter:
                        json_obj = json.loads(payload)
                        json_field=parameter["jsonField"]
                        if json_field in json_obj:
                            value= json_obj[json_field]
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



# class mqttModule:

#
#     # _instance = None
#     #
#     # def __new__(cls):
#     #     if cls._instance is None:
#     #         log.info('Creating the mqttModule')
#     #         cls._instance = super(mqttModule, cls).__new__(cls)
#     #     return cls._instance
#
#     def __init__(self):
#         self._client = mqtt.Client()
#         self._client.on_log = self._on_log
#         self._client.on_message = self._on_message
#         self._client.on_connect = self._on_connect
#         self._client.on_disconnect = self._on_disconnect
#         self.on_connection_changes = self._on_connection_changes
#         self._subscribtion = set()
#         self._subscribtion.add(mqttModule.TOPIC_ADVERTISEMENT)
#         self._things = set()
#
#     def start(self, config, things):
#         log.info(f"things= {things}")
#         self._client.connect(config["server"], config["port"])
#         self._client.loop_start()
#         for el in things:
#             if "mac" in el:
#                 self._things.add(el["mac"])
#             for param in el["parameters"]:
#                 self._subscribtion.add(param['topic'])
#         log.debug(f"things= {self._things}")
#         log.debug(f"topics= {self._subscribtion}")
#
#     def _on_connection_changes(self, state):
#         log.info(f"conection state= {state}")
#
#     def _on_log(self, client, userdata, level, buf):
#         log.info(f"log: {buf}")
#
#     def _on_message(self, client, userdata, message):
#         # msg_dict=json.loads(message.payload.decode("utf-8"))
#         msg = message.payload.decode("utf-8")
#         log.info(f"message received  {msg}, topic={message.topic}, retained {message.retain}")
#         if mqttModule.TOPIC_ADVERTISEMENT is message.topic:
#             self._on_advertisement(msg)
#
#         # if message.topic in self._subscribtion:
#         #     for hander in self._subscribtion[message.topic]:
#         #         hander(msg)
#         if message.retain == 1:
#             log.info("This is a retained message")
#         pass
#
#     def _on_connect(self, client, userdata, flags, rc):
#         if rc == 0:
#             log.info("connected OK")
#             for topic in self._subscribtion:
#                 self._subscribe(topic)
#             self.on_connection_changes(True)
#             self._client.publish(mqttModule.TOPIC_CMD, mqttModule.CMD_ADVERTISEMENT)
#         else:
#             log.info("Bad connection Returned code=", rc)
#
#     def _on_disconnect(self, client, userdata, rc):
#         log.info(f"disconnecting reason {str(rc)}")
#         self.on_connection_changes(False)
#
#     def _on_advertisement(self, message: str):
#         advertisement_dict = json.loads(message)
#         log.debug(f"advertisement= {advertisement_dict}")
#         if "mac" in advertisement_dict and advertisement_dict["mac"] not in self._things:
#             log.warning(f"new thing= mac:{advertisement_dict["mac"]}")
#
#     def _subscribe(self, topic):
#         if self._client.is_connected():
#             log.info(f"mqtt subscribe topic {topic}");
#             self._client.subscribe(topic)
#
#     def subscribe(self, topic: str):
#         self._subscribtion.add(topic)
#         self._subscribe(topic)


class CMQTTThing(CCollectorThing):
    def __init__(self, name, topic: str, masks: set, config: dict):
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
    def __init__(self, name, topic, masks: set, config: dict):
        super().__init__(name, topic, masks, config)
        self._collector.add_field({"temperature", "humidity", "pressure", "ambient_light", "battery"})
        self._collector.set_period(24 * 30)
        self._collector.finalise()

    def _on_message(self, msg):
        super()._on_message(msg)
        if "weather" in msg:
            weather = msg["weather"]
            set_if_present(self._collector_tmp, "pressure", weather)
            set_if_present(self._collector_tmp, "humidity", weather)
            set_if_present(self._collector_tmp, "temperature", weather)
            set_if_present(self._collector_tmp, "ambient_light", weather)
        set_if_present(self._collector_tmp, "battery", msg)


class CClock(CMQTTThing):
    def __init__(self, name, topic, masks: set, config: dict):
        super().__init__(name, topic, masks, config)
        self._collector.add_field({"temperature", "humidity"})
        self._collector.set_period(24 * 2)
        self._collector.finalise()

    def _on_message(self, msg):
        super()._on_message(msg)
        set_if_present(self._collector_tmp, "humidity", msg)
        set_if_present(self._collector_tmp, "temperature", msg)
