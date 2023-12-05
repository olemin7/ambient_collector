
import time
import logging
from thing import CCollectorThing, CObserver
from collector import collector
from typing import Callable

log= logging.getLogger('logger')
class CAliveTracker(CCollectorThing):
    def __init__(self, name, masks:set, config:dict):
        super().__init__(name,config["persistance_dir"])
        self.add_masks(masks)
        self.__on_change = CObserver()
        self._collector.add_field( {"state"})
        self._collector.set_period(7 * 24)
        self._collector.finalise()
        self.__curs_state=None

    def update(self, data):
        if "period" not in self._data:
            self._data["period"] = 5*60
        if "upd_period" in data:
            if self._data["period"]<data["upd_period" ]:
                self._data["period"]=data["upd_period" ]
        self._set_state(1)

    def _set_state(self, state:int):
        if state:
            self._data["timeout"] = int(time.time()+self._data["period"]*3/2)

        if not self.__curs_state or self.__curs_state != state:
            log.info(f"new state = {state}")
            self.__curs_state=state
            self._collector_tmp={"state":state}
            self.__on_change.call(self.get_data())
            if 0 == state:
                self._data.pop("period")
                self._data.pop("timeout")
        self._update()

    def refresh(self):
        if "timeout" in self._data and time.time()>self._data[ "timeout"]:
            self._set_state(0)

    def on_change(self,cb:Callable):
        self.__on_change.subscribe(cb)



