import logging
import time
from typing import Callable

log = logging.getLogger('logger')

class CObserver:
    def __init__(self):
        self.__subscribers = []

    def subscribe(self, cb: Callable):
        self.__subscribers.append(cb)

    def call(self, data):
        for listener in self.__subscribers:
            listener(data)
class CThing:
    object_id=0
    def __init__(self,name:str, masks:set):
        CThing.object_id += 1
        self._data = {}
        self._data["name"]=name
        self._data["id"] = CThing.object_id
        self._data["masks"] = masks
        self.__observer = CObserver()

    def _update(self):
        self._data["updated"] = int(time.time())
        self.__observer.call(self.get_data())

    def get_name(self):
        return self._data["name"]

    def get_data(self):
        return self._data

    def get_id(self):
        return self._data["id"]

    def get_masks(self):
        return  self._data["masks"]

    def on_update(self, cb:Callable):
        self.__observer.subscribe(cb)


