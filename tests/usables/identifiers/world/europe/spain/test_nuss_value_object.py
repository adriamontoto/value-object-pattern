"""
Test NussValueObject value object.
"""

from typing import Any

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.identifiers.world.europe.spain import NussValueObject


def _nuss_value(*, province: str, sequential: str) -> str:
    """
    Build a valid Spanish NUSS value.
    """
    control = int(f'{province}{sequential.zfill(8)}') % 97

    return f'{province}/{sequential}/{control:02d}'


@mark.unit_testing
def test_nuss_value_object_seven_digit_sequential_happy_path() -> None:
    """
    Test NussValueObject value object accepts seven-digit sequential values.
    """
    nuss_value = NussValueObject(value=_nuss_value(province='28', sequential='1234567'))

    assert type(nuss_value.value) is str
    assert nuss_value.value.startswith('281234567')
    assert NussValueObject.identification_regex().fullmatch(_nuss_value(province='28', sequential='1234567'))
    assert NussValueObject.validation_regex().fullmatch(nuss_value.value)


@mark.unit_testing
def test_nuss_value_object_eight_digit_sequential_happy_path() -> None:
    """
    Test NussValueObject value object accepts eight-digit sequential values.
    """
    nuss_value = NussValueObject(value=_nuss_value(province='28', sequential='12345678'))

    assert nuss_value.value.startswith('2812345678')


@mark.unit_testing
def test_nuss_value_object_invalid_value() -> None:
    """
    Test NussValueObject value object raises ValueError when value is not a Spanish Social Security Number.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'NussValueObject value <<<not-a-nuss>>> is not a valid Spanish Social Security Number.',
    ):
        NussValueObject(value='not-a-nuss')


@mark.unit_testing
def test_nuss_value_object_invalid_province_code() -> None:
    """
    Test NussValueObject value object raises ValueError when province code is invalid.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'NussValueObject value <<<99/1234567/00>>> is not a valid Spanish Social Security Number.',
    ):
        NussValueObject(value='99/1234567/00')


@mark.unit_testing
def test_nuss_value_object_invalid_control_value() -> None:
    """
    Test NussValueObject value object raises ValueError when control value is invalid.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'NussValueObject value <<<28/1234567/00>>> is not a valid Spanish Social Security Number.',
    ):
        NussValueObject(value='28/1234567/00')


@mark.unit_testing
def test_nuss_value_object_invalid_processed_value() -> None:
    """
    Test NussValueObject defensive validation branch for invalid processed values.
    """
    nuss_value: Any = NussValueObject(value=_nuss_value(province='28', sequential='1234567'))

    with assert_raises(
        expected_exception=ValueError,
        match=r'NussValueObject value <<<.*>>> is not a valid Spanish Social Security Number.',
    ):
        nuss_value._ensure_value_follows_validation_regex(value=nuss_value.value, processed_value='INVALID')
