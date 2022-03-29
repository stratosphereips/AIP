import pytest

from aip.data.access import get_attacks
from datetime import date

def test_get_attacks():
    """
    Verifies that the get_attacks funtion is working correctly.
    """
    attacks = get_attacks(start=date(2022,3,1), end=date(2022,3,3))
    assert len(attacks) == 3
    assert len(attacks[0]) >= 1
