"""
Test VinValueObject value object.
"""

from typing import Any

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.identifiers.world import VinValueObject


@mark.unit_testing
def test_vin_value_object_happy_path() -> None:
    """
    Test VinValueObject value object happy path.
    """
    raw_value = '1hgbh41jxmn109186'
    expected_value = '1HGBH41JXMN109186'

    vin = VinValueObject(value=raw_value)

    assert type(vin.value) is str
    assert vin.value == expected_value
    assert VinValueObject.identification_regex().fullmatch(raw_value)
    assert VinValueObject.validation_regex().fullmatch(expected_value)


@mark.unit_testing
def test_vin_value_object_invalid_value() -> None:
    """
    Test VinValueObject value object raises ValueError when value is not a valid VIN.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'VinValueObject value <<<1HGBH41JXMN10918I>>> is not a valid Vehicle Identification Number.',
    ):
        VinValueObject(value='1HGBH41JXMN10918I')


@mark.unit_testing
def test_vin_value_object_invalid_processed_value() -> None:
    """
    Test VinValueObject defensive validation branch for invalid processed values.
    """
    vin: Any = VinValueObject(value='1hgbh41jxmn109186')

    with assert_raises(
        expected_exception=ValueError,
        match=r'VinValueObject value <<<1HGBH41JXMN109186>>> is not a valid Vehicle Identification Number.',
    ):
        vin._ensure_value_follows_validation_regex(value='1HGBH41JXMN109186', processed_value='INVALID')
