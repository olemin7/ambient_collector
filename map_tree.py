import logging

log = logging.getLogger('logger')

class MapTree:
    def __init__(self,separator:str ="."):
        self._separator=separator
        self.tree = {}

    def set(self, key:str, value:object):
        keys = key.split(self._separator)
        current = self.tree
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value

    def get(self, key:str=None)->object:
        if key is None:
            return self.tree
        keys = key.split(".")
        current = self.tree
        for k in keys:
            if k not in current:
                return None
            current = current[k]
        return current

    def display(self, current=None, indent=0):
        if current is None:
            current = self.tree
        for key, value in current.items():
            print(" " * indent + key + (":" if isinstance(value, dict) else f": {value}"))
            if isinstance(value, dict):
                self.display(value, indent + 2)


if __name__ == "__main__":
    logging.basicConfig(format=' %(levelname)s %(asctime)s:%(filename)s:%(lineno)d: %(message)s', level=logging.DEBUG)

