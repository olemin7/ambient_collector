import logging
import statistics as s
import numbers

log = logging.getLogger('logger')

def to_type(value, data_type):
    if data_type is not None:
        if data_type == "float1":
            return round(float(value), 1)
        elif data_type == "float2":
            return round(float(value), 2)
        elif data_type == "int":
            return int(value)
    return value

def transformation(vals, arg: object) -> list[dict]:
    span = arg.get("span", 60 * 60)
    mode = arg["mode"]
    data_type = arg.get("to_type")
    if mode is None:
        return None
    spanned = {}
    for element in vals:
        ts = int(element["ts"] / span) * span
        if isinstance(element["value"], numbers.Number):
            if ts not in spanned:
                spanned[ts] = []
            spanned[ts].append(element["value"])
    out = []
    for k, v in spanned.items():
        val = {"ts": k}
        if "min" in mode:
            val["min"] = to_type(min(v), data_type)
        if "max" in mode:
            val["max"] = to_type(max(v), data_type)
        if "avr" in mode:
            val["avr"] = to_type(s.mean(v), data_type)
        out.append(val)
    log.info(f"input count={len(vals)}, output={len(out)}")
    return out
