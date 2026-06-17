"""
Test ImeiValueObject value object.
"""

from typing import Any

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.internet.mobile import ImeiValueObject


@mark.unit_testing
def test_imei_value_object_happy_path() -> None:
    """
    Test ImeiValueObject value object happy path.
    """
    imei = ImeiValueObject(value='490-154-203-237-518')

    assert type(imei.value) is str
    assert imei.value == '490154203237518'
    assert ImeiValueObject.identification_regex().fullmatch('490-154-203-237-518')
    assert ImeiValueObject.validation_regex().fullmatch(imei.value)


@mark.unit_testing
def test_imei_value_object_luhn_checksum() -> None:
    """
    Test ImeiValueObject Luhn checksum helper.
    """
    imei = ImeiValueObject(value='490-154-203-237-518')

    assert imei._validate_luhn_checksum(imei='490154203237518')
    assert not imei._validate_luhn_checksum(imei='490154203237519')


@mark.unit_testing
def test_imei_value_object_invalid_value() -> None:
    """
    Test ImeiValueObject value object raises ValueError when value is not an IMEI.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'ImeiValueObject value <<<invalid>>> is not a valid International Mobile Equipment Identity.',
    ):
        ImeiValueObject(value='invalid')


@mark.unit_testing
def test_imei_value_object_invalid_luhn_checksum() -> None:
    """
    Test ImeiValueObject value object raises ValueError when Luhn checksum is invalid.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'ImeiValueObject value <<<490154203237519>>> is not a valid International Mobile Equipment Identity.',
    ):
        ImeiValueObject(value='490154203237519')


@mark.unit_testing
def test_imei_value_object_invalid_processed_value() -> None:
    """
    Test ImeiValueObject defensive validation branch for invalid processed values.
    """
    imei: Any = ImeiValueObject(value='490-154-203-237-518')

    with assert_raises(
        expected_exception=ValueError,
        match=r'ImeiValueObject value <<<490154203237518>>> is not a valid International Mobile Equipment Identity.',
    ):
        imei._ensure_value_follows_validation_regex(value=imei.value, processed_value='INVALID')
