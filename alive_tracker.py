
import time
import logging
from thing import  CObserver
from mqtt_module import CMQTTThing
from typing import Callable

log= logging.getLogger('logger')
class CAliveTracker(CMQTTThing):
    def __init__(self, name,topic, masks:set, config:dict):
        super().__init__(name,topic,masks,config)
        self.__on_change = CObserver()
        self._collector.add_field( {"state"})
        self._collector.set_period(7 * 24)
        self._collector.finalise()
        self._data["timeout"] = int(time.time() + 30)

    def on_message(self, data):
        if "upd_period" in data:
            timeout = int(time.time()+data["upd_period"]+5)
            if ("timeout" not in self._data) or (self._data["timeout"] < timeout):
                self._data["timeout"] = timeout
                self._set_state(1)
        else:
            log.error(f"no upd_period in data={data}")

    def _set_state(self, state:int):
        if ("state" not in self._data) or self._data["state"] != state:
            log.info(f"new state = {state}")
            self._data["state"]=state
            self._collector_tmp={"state":state}
            self.__on_change.call(self.get_data())
        self._update()

    def refresh(self):
        if "timeout" in self._data and time.time()>self._data["timeout"]:
            self._data.pop("timeout")
            self._set_state(0)

    def on_change(self,cb:Callable):
        self.__on_change.subscribe(cb)



