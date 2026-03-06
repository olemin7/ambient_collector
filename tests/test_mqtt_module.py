import pytest
from mqtt_module import MQTTThings


@pytest.mark.parametrize("payload,parameter,result", [
    ("10", {}, "10"),
    ("10", {'field': "f0"}, None),
    ('{"f0":10}', {'field': "f0"}, 10),
    ('{"f0":{"f1":10}}', {'field': "f0.f1"}, 10),
    ('{"f0":{"f1":10}}', {'field': "f0.f3"}, None),
    ('{"f0":{"f1":10}}', {'field': "f0.f1.f3"}, None),
])
def test_parse_field(payload, parameter, result):
    assert MQTTThings.parse_field(payload, parameter) == result
