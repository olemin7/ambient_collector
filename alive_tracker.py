
import time
import logging
from thing import CThing
from collector import add_record, get_latest_record, ts_to_str

log= logging.getLogger('logger')
class CAliveTracker(CThing):
    def __init__(self, name, masks:set):
        super().__init__(name, masks)

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
        curs_state =get_latest_record(self._data,"state")
        if curs_state and curs_state["value"]== state:
            return
        log.info(f"new state = {state}")
        add_record(self._data, "state", state, 7 * 24 * 60 * 60)
        if 0 == state:
            self._data.pop("period")
            self._data.pop("timeout")
        self._update()

    def refresh(self):
        if "timeout" in self._data and time.time()>self._data[ "timeout"]:
            self._set_state(0)


