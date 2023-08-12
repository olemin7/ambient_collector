
from collector import *
import RPi.GPIO as GPIO

V220_PIN = 17
V220_INVERT = 0
LOW_BAT_PIN = 21
LOW_BAT_INVERT = 0

class CGPIOpsu:
    def __init__(self,cb):
        self._data = {}
        self._data["name"]="PSU"
        self.__cb=cb
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(V220_PIN, GPIO.IN)
        GPIO.setup(LOW_BAT_PIN, GPIO.IN)
        self.__update()
        GPIO.add_event_callback(gpio=V220_PIN,bouncetime=200,callback=self.__on_event)
        GPIO.add_event_callback(gpio=V220_PIN, bouncetime=200, callback=self.__on_event)
        pass
    def __update(self):
        self._data["V220"] = GPIO.input(V220_PIN)
        self._data["LOW_BAT"] = GPIO.input(LOW_BAT_PIN)
        pass

    def __on_event(self):
        self.__update()
        self.__cb(self._data)
        pass

    def get_name(self):
        return self._data["name"]
    def get_name(self):
        return self._data["name"]
    def get_data(self):
        return self._data

    pass

if __name__ == "__main__":
    def print_state(vals):
        print(vals)
        pass
    psu=CGPIOpsu(print_state)
    while 1:
        pass
