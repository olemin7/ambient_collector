import pytest
from map_tree import MapTree


def test_basic():
    tree = MapTree()
    tree.set("a.b.c", 1)
    tree.set("a.b.d", 2)
    tree.set("a.e", 3)
    tree.set("x.y", 4)
    assert tree.get("a.b.c") == 1
    assert tree.get("a.b") == {'c': 1, 'd': 2}
    assert tree.get("x.y") == 4
    assert tree.get("non.existent") is None


@pytest.mark.parametrize("field,value", [("a.b.c", 1), ("a.b.d", 2), ("a.e", 3)])
def test_snake(field, value):
    tree = MapTree()
    tree.set(field, value)
    assert tree.get(field) == value


def test_update():
    tree = MapTree()
    field = "x.y.z"
    tree.set(field, 1)
    tree.set(field, 2)
    assert tree.get(field) == 2
