import logging
import os
import pytest
import statistics as s
log = logging.getLogger('logger')

def to_type(value,data_type):
    if data_type is not None:
        if data_type == "float1":
            return round(float(value), 1)
        elif data_type == "float2":
            return round(float(value), 2)
        elif data_type == "int":
            return int(value)
    return value

def tranformation(vals,arg:object)->[{}]:
    span = arg["span"]if "span" in arg else 60*60   #hour
    mode=arg["mode"]
    data_type = arg["to_type"] if "to_type" in arg else None
    if mode is None:
        return None
    spanned={}
    for element in vals:
        ts=int(element["ts"]/span)*span
        if ts not in spanned:
            spanned[ts]=[]
        spanned[ts].append(element["value"])
    out =[]
    for k, v in spanned.items():
        val={"ts":k}
        if "min" in mode:
            val["min"]=to_type(min(v),data_type)
        if "max" in mode:
            val["max"]=to_type(max(v),data_type)
        if "avr" in mode:
            val["avr"]=to_type(s.mean(v),data_type)
        out.append(val)
    log.info(f"input count={len(vals)}, output={len(out)}")
    return  out

@pytest.fixture
def default_vars():
     return [
        {'ts': 0, 'value': 1},
        {'ts': 60*60*1/4, 'value': 2},
        {'ts': 60*60*2/4, 'value': 3},
        {'ts': 60*60*3/4, 'value': 4},
        {'ts': 60*60*4/4, 'value': 5},
        {'ts': 60*60*5/4, 'value': 6},
        {'ts': 60*60*6/4, 'value': 7},
        {'ts': 60*60*7/4, 'value': 8},]


@pytest.mark.parametrize("arg,expected",[
    ({"mode":["max"]},[{'ts': 0, 'max': 4}, {'ts': 3600, 'max': 8}]),
    ({"mode":["min"]},[{'ts': 0, 'min': 1}, {'ts': 3600, 'min': 5}]),
    ({"mode":["min","max"]},[{'ts': 0, 'min': 1,'max':4}, {'ts': 3600, 'min': 5, 'max': 8}]),
])
def test_basic(default_vars,arg,expected):
    assert tranformation(default_vars,arg)==expected

@pytest.mark.parametrize("arg,expected",[
    ({"mode":["avr"]},[{'ts': 0, 'avr': 2.5}, {'ts': 3600, 'avr': 6.5}]),
    ])
def test_basic(default_vars,arg,expected):
    assert tranformation(default_vars,arg)==expected



