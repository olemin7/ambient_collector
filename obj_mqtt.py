import json
from collector import *

class CWeather:
    def __init__(self,name,topic,event):
        self.__name=name
        self.__topic=topic
        self.__event= event
        self.__data={}
        pass

    def on_message(self,msg):
        if "bmp180" in msg:
            add_value(self.__data, "pressure", msg["bmp180"], "pressure", 7 * 24 * 60 * 60)
            pass
        if "dht" in msg:
            set_value(self.__data,"humidity", msg["dht"], "humidity")
            add_value(self.__data,"temperature", msg["dht"], "temperature",7*24*60*60)
            pass
        if "battery" in msg:
            set_value(self.__data,"battery", msg["battery"], "value")
            pass
        if "BH1750" in msg:
            set_value(self.__data,"lighting", msg["BH1750"], "value")
            pass
        if "wifi" in msg:
            set_value(self.__data, "rssi", msg["wifi"], "rssi")
            pass
        pass

    def get_name(self):
        return self.__name
    def get_topic(self):
        return self.__topic
    def get_event(self):
        return self.__event
    def get_data(self):
        return self.__data
    pass

class CClock:
    def __init__(self,name,topic,event):
        self.__name=name
        self.__topic=topic
        self.__event= event
        self.__data={}
        pass

    def on_message(self,msg):
        set_value(self.__data, "temperature", msg, "temperature")
        set_value(self.__data, "humidity", msg, "humidity")
        set_value(self.__data, "rssi", msg, "rssi")
        print(msg)
        pass

    def get_name(self):
        return self.__name
    def get_topic(self):
        return self.__topic
    def get_event(self):
        return self.__event
    def get_data(self):
        return self.__data
    pass

