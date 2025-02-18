import logging
import pytest
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

def test_basic():
    tree = MapTree()
    tree.set("a.b.c", 1)
    tree.set("a.b.d", 2)
    tree.set("a.e", 3)
    tree.set("x.y", 4)
    print(tree.get("a.b.c"))  # Output: 1
    print(tree.get("a.b"))  # Output: {'c': 1, 'd': 2}
    print(tree.get("x.y"))  # Output: 4
    print(tree.get("non.existent"))  # Output: None
    tree.display()
    print(tree.get())


@pytest.mark.parametrize("field,value", [("a.b.c", 1), ("a.b.d", 2), ("a.e", 3)])
def test_snake(field,value):
    tree = MapTree()
    tree.set(field, value)
    assert tree.get(field) == value

def test_update():
    tree = MapTree()
    field="x.y.z"
    tree.set(field, 1)
    tree.set(field, 2)
    assert tree.get(field) == 2

