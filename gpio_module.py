
from collector import *
import RPi.GPIO as GPIO

V220_PIN = 11
LOW_BAT_PIN = 23

class CGPIOpsu:
    def __init__(self):
        self._data = {}
        self._data["name"]="PSU"
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(V220_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(LOW_BAT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.__update()
        GPIO.add_event_detect(V220_PIN, GPIO.BOTH,callback = self.__on_event, bouncetime = 200)
        GPIO.add_event_detect(LOW_BAT_PIN, GPIO.BOTH,callback = self.__on_event, bouncetime = 200)
        pass
    def __update(self):
        self._data["V220"] = GPIO.input(V220_PIN)
        self._data["BAT_OK"] = GPIO.input(LOW_BAT_PIN)
        pass

    def __on_event(self,pin_no):
        self.__update()
        if self.__cb:
            self.__cb(self._data)
            pass
        pass

    def set_cb(self,cb):
        self.__cb=cb
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
