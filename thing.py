import logging

log= logging.getLogger('logger')

class CThing:
    object_id=0
    def __init__(self,name:str,topic:str, masks:set):
        CThing.object_id += 1
        self._data = {}
        self._data["name"]=name
        self._data["topic"] = topic
        self._data["id"] = CThing.object_id
        self._data["masks"] = masks
        pass
    def get_name(self):
        return self._data["name"]
    def get_topic(self):
        return self._data["topic"]
    def get_data(self):
        return self._data
    def get_id(self):
        return self._data["id"]

    def get_masks(self):
        return  self._data["masks"]
