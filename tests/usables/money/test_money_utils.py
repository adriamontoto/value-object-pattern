"""
Test money utility functions.
"""

from pytest import mark

from value_object_pattern.usables.money import utils as money_utils
from value_object_pattern.usables.utils import validate_luhn_checksum


@mark.unit_testing
def test_money_utils_load_iban_lengths() -> None:
    """
    Test money utility functions load IBAN lengths.
    """
    money_utils.get_iban_lengths.cache_clear()

    assert money_utils.get_iban_lengths()['GB'] == 22


@mark.unit_testing
def test_validate_luhn_checksum() -> None:
    """
    Test shared Luhn checksum validation helper.
    """
    assert validate_luhn_checksum(value='4111111111111111')
    assert not validate_luhn_checksum(value='4111111111111112')
