import pytest
from collector import Collector


@pytest.fixture
def default_cfg():
    parameters = [{"name": "par0"}, {"name": "pers0", "retention": 100}]
    things = [{"name": "name0", "parameters": parameters}]
    return {
        "persistence_dir": "./test",
        "things": things,
    }


def test_basic(default_cfg):
    c = Collector(default_cfg)
    assert c.get_fields() is not None


def test_write_new(default_cfg):
    c = Collector(default_cfg)
    c.set("name0.pers0", 42)
    assert c.get_fields() is not None
