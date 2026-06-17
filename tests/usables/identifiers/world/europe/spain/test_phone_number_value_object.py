"""
Test PhoneNumberValueObject value object.
"""

from typing import Any

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.identifiers.world.europe.spain import PhoneNumberValueObject


@mark.unit_testing
def test_phone_number_value_object_formats_country_code_prefix() -> None:
    """
    Test PhoneNumberValueObject value object formats a Spanish phone number with 34 prefix.
    """
    raw_phone = '34 612 345 678'

    phone_number = PhoneNumberValueObject(value=raw_phone)

    assert type(phone_number.value) is str
    assert phone_number.value == '34 612345678'
    assert phone_number.phone_code.value == '34'
    assert PhoneNumberValueObject.identification_regex().fullmatch(raw_phone)
    assert PhoneNumberValueObject.validation_regex().fullmatch(phone_number.value)


@mark.unit_testing
def test_phone_number_value_object_formats_double_zero_prefix() -> None:
    """
    Test PhoneNumberValueObject value object formats a Spanish phone number with 0034 prefix.
    """
    assert PhoneNumberValueObject(value='0034 612 345 678').value == '34 612345678'


@mark.unit_testing
def test_phone_number_value_object_formats_plus_prefix() -> None:
    """
    Test PhoneNumberValueObject value object formats a Spanish phone number with +34 prefix.
    """
    assert PhoneNumberValueObject(value='+34 612 345 678').value == '34 612345678'


@mark.unit_testing
def test_phone_number_value_object_formats_national_number() -> None:
    """
    Test PhoneNumberValueObject value object formats a Spanish phone number without country prefix.
    """
    assert PhoneNumberValueObject(value='612 345 678').value == '34 612345678'


@mark.unit_testing
def test_phone_number_value_object_invalid_value() -> None:
    """
    Test PhoneNumberValueObject value object raises ValueError when value is not a valid Spanish phone number.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'PhoneNumberValueObject value <<<512 345 678>>> is not a valid Spanish phone number.',
    ):
        PhoneNumberValueObject(value='512 345 678')


@mark.unit_testing
def test_phone_number_value_object_invalid_processed_value() -> None:
    """
    Test PhoneNumberValueObject defensive validation branch for invalid processed values.
    """
    phone_number: Any = PhoneNumberValueObject(value='+34 612 345 678')

    with assert_raises(
        expected_exception=ValueError,
        match=r'PhoneNumberValueObject value <<<\+34 612 345 678>>> is not a valid Spanish phone number.',
    ):
        phone_number._ensure_value_follows_validation_regex(value='+34 612 345 678', processed_value='INVALID')
