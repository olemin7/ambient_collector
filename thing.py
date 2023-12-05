import logging
import time
from typing import Callable
from collector import *

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
    def __init__(self,name:str):
        CThing.object_id += 1
        self._data = {}
        self._data["name"]=name
        self._data["id"] = CThing.object_id
        self._data["masks"] = list()
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

    def add_masks(self, masks:set):
        self._data["masks"].extend(masks)

    def get_masks(self,):
        return self._data["masks"]

    def on_update(self, cb:Callable):
        self.__observer.subscribe(cb)


class CCollectorThing(CThing):
    def __init__(self, name:str, path:str):
        super().__init__(name)
        self.add_masks({"collector"})
        self._data["collector"]=[]
        self._collector_tmp = {}
        self._collector = collector(os.path.join(path,name+".csv"), self._data["collector"])

    def _update(self):
        if len(self._collector_tmp):
            self._collector.add(self._collector_tmp)
            self._collector_tmp = {}
        super()._update()

