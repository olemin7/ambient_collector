import json
from collector import *


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
            add_value(self._data, "pressure", msg["bmp180"], "pressure", 7 * 24 * 60 * 60)
            pass
        if "dht" in msg:
            set_value(self._data, "humidity", msg["dht"], "humidity")
            add_value(self._data, "temperature", msg["dht"], "temperature", 7 * 24 * 60 * 60)
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

