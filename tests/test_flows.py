"""
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
"""
#! /usr/local/bin/python3

import pytest

from models.flows import Flow


MOCKED_CSV_LINE_1 = '45.155.205.27','43179','9324221','587.3','51803957','2314.0','384670','27.63','150099154','167666237','1467859853.313'
MOCKED_CSV_LINE_2 = '123.8.185.32',26049,7415310,284.6,41808957,1605.0,284577,10.92,157899154,166699154,1578968762.519

MOCKED_INVALID_CSV_LINE_1 = ('45.155.205.27',26049,'','587.3',41808957,'2314.0',284577,'',157899154,'167666237',1578968762.519)

MOCKED_VALID_DICT_1 = {
    'src_address': '45.155.205.27',
    'events': '43179',
    'duration': '9324221',
    'avg_duration': '587.3',
    'bytes': '51803957',
    'avg_bytes': '2314.0',
    'packets': '384670',
    'avg_packets': '27.63',
    'first_event': '150099154',
    'last_event': '167666237',
    'avg_events': '1467859853.313'
}

MOCKED_VALID_DICT_2 = {
    'src_address': '123.8.185.32',
    'events': 26049,
    'duration': 7415310,
    'avg_duration': 284.6,
    'bytes': 41808957,
    'avg_bytes': 1605.0,
    'packets': 284577,
    'avg_packets': 10.92,
    'first_event': 157899154,
    'last_event': 166699154,
    'avg_events': 1578968762.519
}

MOCKED_INVALID_DICT_1 = {
    'src_address': '45.155.205.27',
    'events': '43179',
    'duration': '9324221',
    'avg_duration': '587.3',
    'bytes': '51803957',
    'packets': '384670',
    'avg_packets': '27.63',
    'first_event': '150099154',
    'last_event': '167666237',
    'avg_events': '1467859853.313'
}

MOCKED_INVALID_DICT_2 = {
    'src_address': '123.8.185.32',
    'events': 26049,
    'duration': 7415310,
    'avg_duration': 284.6,
    'bytes': 41808957,
    'packets': 284577,
    'avg_packets': 10.92,
    'first_event': 157899154,
    'last_event': 166699154,
    'avg_events': 1578968762.519
}

EXPECTED_KEYS_LEN = 11


# Success
def test_flow_instantiation_with_line_v1():
    """
    Verifies that RawRating has correct data types
    """
    assert len(MOCKED_CSV_LINE_1) == EXPECTED_KEYS_LEN
    current_flow = Flow.from_line(MOCKED_CSV_LINE_1)
    assert isinstance(current_flow.src_address, str)
    assert isinstance(current_flow.events, float)
    assert isinstance(current_flow.avg_events, float)
    assert isinstance(current_flow.duration, float)
    assert isinstance(current_flow.avg_duration, float)
    assert isinstance(current_flow.bytes, float)
    assert isinstance(current_flow.avg_bytes, float)
    assert isinstance(current_flow.packets, float)
    assert isinstance(current_flow.avg_packets, float)
    assert isinstance(current_flow.first_event, float)
    assert isinstance(current_flow.last_event, float)
    assert isinstance(current_flow.aged_score, float)


def test_flow_instantiation_with_line_v2():
    """
    Verifies that RawRating has correct data types
    """
    assert len(MOCKED_CSV_LINE_2) == EXPECTED_KEYS_LEN
    current_flow = Flow.from_line(MOCKED_CSV_LINE_2)
    assert isinstance(current_flow.src_address, str)
    assert isinstance(current_flow.events, float)
    assert isinstance(current_flow.avg_events, float)
    assert isinstance(current_flow.duration, float)
    assert isinstance(current_flow.avg_duration, float)
    assert isinstance(current_flow.bytes, float)
    assert isinstance(current_flow.avg_bytes, float)
    assert isinstance(current_flow.packets, float)
    assert isinstance(current_flow.avg_packets, float)
    assert isinstance(current_flow.first_event, float)
    assert isinstance(current_flow.last_event, float)
    assert isinstance(current_flow.aged_score, float)


def test_flow_instantiation_with_dict_v1():
    """
    Verifies that RawRating instantiates successfdully and
    has correct data types when all required keys are present
    even with str values
    """
    assert len(MOCKED_VALID_DICT_1.keys()) == EXPECTED_KEYS_LEN
    current_flow = Flow.from_dict(MOCKED_VALID_DICT_1)
    assert isinstance(current_flow.src_address, str)
    assert isinstance(current_flow.events, float)
    assert isinstance(current_flow.avg_events, float)
    assert isinstance(current_flow.duration, float)
    assert isinstance(current_flow.avg_duration, float)
    assert isinstance(current_flow.bytes, float)
    assert isinstance(current_flow.avg_bytes, float)
    assert isinstance(current_flow.packets, float)
    assert isinstance(current_flow.avg_packets, float)
    assert isinstance(current_flow.first_event, float)
    assert isinstance(current_flow.last_event, float)
    assert isinstance(current_flow.aged_score, float)


def test_flow_instantiation_with_dict_v2():
    """
    Verifies that RawRating instantiates successfdully and
    has correct data types when all required keys are present
    while having float values
    """
    assert len(MOCKED_VALID_DICT_2.keys()) == EXPECTED_KEYS_LEN
    current_flow = Flow.from_dict(MOCKED_VALID_DICT_2)
    assert isinstance(current_flow.src_address, str)
    assert isinstance(current_flow.events, float)
    assert isinstance(current_flow.avg_events, float)
    assert isinstance(current_flow.duration, float)
    assert isinstance(current_flow.avg_duration, float)
    assert isinstance(current_flow.bytes, float)
    assert isinstance(current_flow.avg_bytes, float)
    assert isinstance(current_flow.packets, float)
    assert isinstance(current_flow.avg_packets, float)
    assert isinstance(current_flow.first_event, float)
    assert isinstance(current_flow.last_event, float)
    assert isinstance(current_flow.aged_score, float)

# Failure
def test_failed_flow_instantiation():
    """
    Verifies that Flow fails instantiation if missing dict
    """
    with pytest.raises(Exception) as e:
        return Flow.from_dict()


def test_failed_flow_instantiation_from_line_v1():
    """
    Verifies that Flow fails instantiation if missing line
    """
    with pytest.raises(Exception) as e:
        return Flow.from_line()


def test_failed_flow_instantiation_from_line_v1():
    """
    Verifies that Flow fails instantiation with TypeError
    """
    with pytest.raises(ValueError) as e:
        return Flow.from_line(MOCKED_INVALID_CSV_LINE_1)


def test_failed_flow_instantiation_from_dict_v2():
    """
    Verifies that Flow fails instantiation with TypeError
    """
    with pytest.raises(TypeError) as e:
        return Flow.from_dict(MOCKED_INVALID_DICT_1)


def test_failed_flow_instantiation_from_dict_v2():
    """
    Verifies that Flow fails instantiation with TypeError
    """
    with pytest.raises(TypeError) as e:
        return Flow.from_dict(MOCKED_INVALID_DICT_2)
