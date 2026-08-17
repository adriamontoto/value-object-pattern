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
def test_iban_value_object_accepts_valid_spanish_bban_control_digits() -> None:
    """
    Test IbanValueObject accepts a Spanish IBAN with valid CCC control digits.
    """
    iban = IbanValueObject(value='ES9121000418450200051332')

    assert iban.value == 'ES9121000418450200051332'


@mark.unit_testing
def test_iban_value_object_invalid_value() -> None:
    """
    Test IbanValueObject value object raises ValueError when value is not an IBAN.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'IbanValueObject value is not a valid International Bank Account Number.',
    ):
        IbanValueObject(value='invalid')


@mark.unit_testing
def test_iban_value_object_invalid_country_code() -> None:
    """
    Test IbanValueObject value object raises ValueError when country code is unknown.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'IbanValueObject value is not a valid International Bank Account Number.',
    ):
        IbanValueObject(value='ZZ82WEST12345698765432')


@mark.unit_testing
def test_iban_value_object_invalid_length() -> None:
    """
    Test IbanValueObject value object raises ValueError when length is invalid for the country code.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'IbanValueObject value is not a valid International Bank Account Number.',
    ):
        IbanValueObject(value='GB82WEST')


@mark.unit_testing
def test_iban_value_object_invalid_mod97_checksum() -> None:
    """
    Test IbanValueObject value object raises ValueError when MOD-97 checksum is invalid.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'IbanValueObject value is not a valid International Bank Account Number.',
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
        match=r'IbanValueObject value is not a valid International Bank Account Number.',
    ):
        iban._ensure_value_follows_validation_regex(value='GB82WEST12345698765432', processed_value='INVALID')


@mark.unit_testing
def test_iban_value_object_rejects_spanish_bban_with_invalid_ccc_control_digits() -> None:
    """
    Test IbanValueObject rejects a Spanish IBAN whose MOD-97 checksum is valid but CCC digits are invalid.
    """
    invalid_iban = 'ES2921000418460200051332'
    valid_iban = IbanValueObject(value='GB82WEST12345698765432')

    assert valid_iban._validate_mod97_checksum(iban=invalid_iban)

    with assert_raises(
        expected_exception=ValueError,
        match=r'IbanValueObject value is not a valid International Bank Account Number.',
    ) as error:
        IbanValueObject(value=invalid_iban)

    assert invalid_iban not in str(error.value)


@mark.unit_testing
def test_iban_value_object_validates_spanish_bban_shape_and_control_digits() -> None:
    """
    Test Spanish BBAN validation rejects malformed and incorrect control-digit inputs.
    """
    assert IbanValueObject._validate_spanish_bban(bban='21000418450200051332')
    assert not IbanValueObject._validate_spanish_bban(bban='21000418460200051332')
    assert not IbanValueObject._validate_spanish_bban(bban='short')
    assert not IbanValueObject._validate_spanish_bban(bban='2100041845020005133A')


@mark.unit_testing
def test_iban_value_object_spanish_control_digit_maps_special_results() -> None:
    """
    Test Spanish control-digit calculations map 10 to 1 and 11 to 0.
    """
    assert IbanValueObject._spanish_control_digit(digits='1000000000', weights=(1, 2, 4, 8, 5, 10, 9, 7, 3, 6)) == 1
    assert IbanValueObject._spanish_control_digit(digits='00000000', weights=(4, 8, 5, 10, 9, 7, 3, 6)) == 0
