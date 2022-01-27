"""
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
"""
#! /usr/local/bin/python3

import pytest

from models.metric_weights import MetricWeights
from slips_aip_constants.enums import Weights


def test_normalized_weight():
    """
    Verifies that Weights.ORIGINAL has correct values
    """
    current_normalized_weight = Weights.NORMALIZED.value
    assert isinstance(current_normalized_weight, MetricWeights)
    FIVE_PERCENTAGE = 0.05
    TWENTY_PERCENTAGE = 0.20
    assert current_normalized_weight.total_events == FIVE_PERCENTAGE
    assert current_normalized_weight.average_events == TWENTY_PERCENTAGE
    assert current_normalized_weight.total_duration == FIVE_PERCENTAGE
    assert current_normalized_weight.average_duration == TWENTY_PERCENTAGE
    assert current_normalized_weight.total_bytes == FIVE_PERCENTAGE
    assert current_normalized_weight.average_bytes == TWENTY_PERCENTAGE
    assert current_normalized_weight.total_packets == FIVE_PERCENTAGE
    assert current_normalized_weight.average_packets == TWENTY_PERCENTAGE


def test_original_weight():
    """
    Verifies that Weights.NORMALIZED has correct values
    """
    current_original_weight = Weights.ORIGINAL.value
    assert isinstance(current_original_weight, MetricWeights)
    TEN_PERCENTAGE = 0.10
    TWENTY_PERCENTAGE = 0.20
    assert current_original_weight.total_events == TWENTY_PERCENTAGE
    assert current_original_weight.average_events == TEN_PERCENTAGE
    assert current_original_weight.total_duration == TEN_PERCENTAGE
    assert current_original_weight.average_duration == TEN_PERCENTAGE
    assert current_original_weight.total_bytes == TWENTY_PERCENTAGE
    assert current_original_weight.average_bytes == TEN_PERCENTAGE
    assert current_original_weight.total_packets == TEN_PERCENTAGE
    assert current_original_weight.average_packets == TEN_PERCENTAGE


def test_weights_length():
    """
    Verifies that there are TWO (2) accepted Weights
    """
    assert len(Weights) == 2
