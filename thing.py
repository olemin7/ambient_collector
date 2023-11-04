import logging
import time
from typing import Callable

log= logging.getLogger('logger')

class CThing:
    object_id=0
    def __init__(self,name:str, masks:set):
        CThing.object_id += 1
        self._data = {}
        self._data["name"]=name
        self._data["id"] = CThing.object_id
        self._data["masks"] = masks
        self.__subscribers=[]
    def _update(self):
        self._data["updated"] = int(time.time())
        for listener in self.__subscribers:
            listener(self.get_data())
    def get_name(self):
        return self._data["name"]
    def get_data(self):
        return self._data
    def get_id(self):
        return self._data["id"]
    def get_masks(self):
        return  self._data["masks"]
    def subscribe(self,cb:Callable):
        self.__subscribers.append(cb)


