import pytest
from transformation import transformation


@pytest.fixture
def default_vars():
    return [
        {'ts': 0, 'value': 1},
        {'ts': 60 * 60 * 1 / 4, 'value': 2},
        {'ts': 60 * 60 * 2 / 4, 'value': 3},
        {'ts': 60 * 60 * 3 / 4, 'value': 4},
        {'ts': 60 * 60 * 4 / 4, 'value': 5},
        {'ts': 60 * 60 * 5 / 4, 'value': 6},
        {'ts': 60 * 60 * 6 / 4, 'value': 7},
        {'ts': 60 * 60 * 7 / 4, 'value': 8},
    ]


@pytest.mark.parametrize("arg,expected", [
    ({"mode": ["max"]}, [{'ts': 0, 'max': 4}, {'ts': 3600, 'max': 8}]),
    ({"mode": ["min"]}, [{'ts': 0, 'min': 1}, {'ts': 3600, 'min': 5}]),
    ({"mode": ["min", "max"]}, [{'ts': 0, 'min': 1, 'max': 4}, {'ts': 3600, 'min': 5, 'max': 8}]),
])
def test_min_max(default_vars, arg, expected):
    assert transformation(default_vars, arg) == expected


@pytest.mark.parametrize("arg,expected", [
    ({"mode": ["avr"]}, [{'ts': 0, 'avr': 2.5}, {'ts': 3600, 'avr': 6.5}]),
])
def test_avr(default_vars, arg, expected):
    assert transformation(default_vars, arg) == expected
