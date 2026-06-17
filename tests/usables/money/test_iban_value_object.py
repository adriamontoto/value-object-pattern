"""
Test IbanValueObject value object.
"""

from typing import Any

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.money import IbanValueObject


@mark.unit_testing
def test_iban_value_object_happy_path() -> None:
    """
    Test IbanValueObject value object happy path.
    """
    raw_value = 'gb82 west 1234 5698 7654 32'
    expected_value = 'GB82WEST12345698765432'

    iban = IbanValueObject(value=raw_value)

    assert type(iban.value) is str
    assert iban.value == expected_value
    assert IbanValueObject.identification_regex().fullmatch(raw_value)
    assert IbanValueObject.validation_regex().fullmatch(expected_value)


@mark.unit_testing
def test_iban_value_object_invalid_value() -> None:
    """
    Test IbanValueObject value object raises ValueError when value is not an IBAN.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'IbanValueObject value <<<invalid>>> is not a valid International Bank Account Number.',
    ):
        IbanValueObject(value='invalid')


@mark.unit_testing
def test_iban_value_object_invalid_country_code() -> None:
    """
    Test IbanValueObject value object raises ValueError when country code is unknown.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'IbanValueObject value <<<ZZ82WEST12345698765432>>> is not a valid International Bank Account Number.',
    ):
        IbanValueObject(value='ZZ82WEST12345698765432')


@mark.unit_testing
def test_iban_value_object_invalid_length() -> None:
    """
    Test IbanValueObject value object raises ValueError when length is invalid for the country code.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'IbanValueObject value <<<GB82WEST>>> is not a valid International Bank Account Number.',
    ):
        IbanValueObject(value='GB82WEST')


@mark.unit_testing
def test_iban_value_object_invalid_mod97_checksum() -> None:
    """
    Test IbanValueObject value object raises ValueError when MOD-97 checksum is invalid.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'IbanValueObject value <<<GB82WEST12345698765433>>> is not a valid International Bank Account Number.',
    ):
        IbanValueObject(value='GB82WEST12345698765433')


@mark.unit_testing
def test_iban_value_object_invalid_processed_value() -> None:
    """
    Test IbanValueObject defensive validation branch for invalid processed values.
    """
    iban: Any = IbanValueObject(value='gb82 west 1234 5698 7654 32')

    with assert_raises(
        expected_exception=ValueError,
        match=r'IbanValueObject value <<<GB82WEST12345698765432>>> is not a valid International Bank Account Number.',
    ):
        iban._ensure_value_follows_validation_regex(value='GB82WEST12345698765432', processed_value='INVALID')
