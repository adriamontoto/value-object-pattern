"""
Test DniValueObject value object.
"""

from typing import Any

from object_mother_pattern import StringMother
from object_mother_pattern.mothers.identifiers.countries.spain import DniMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.identifiers.world.europe.spain import DniValueObject


@mark.unit_testing
def test_dni_value_object_happy_path() -> None:
    """
    Test DniValueObject value object happy path.
    """
    dni_value = DniValueObject(value=DniMother.create())

    assert type(dni_value.value) is str
    assert dni_value.value.isupper()


@mark.unit_testing
def test_dni_value_object_formats_value() -> None:
    """
    Test DniValueObject value object formats separators and uppercase letters.
    """
    dni_value = DniValueObject(value='87654321-x')

    assert dni_value.value == '87654321X'
    assert DniValueObject.identification_regex().fullmatch('87654321-x')
    assert DniValueObject.validation_regex().fullmatch(dni_value.value)


@mark.unit_testing
def test_dni_value_object_invalid_type() -> None:
    """
    Test DniValueObject value object raises TypeError when value is not an string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'DniValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        DniValueObject(value=DniMother.invalid_type())


@mark.unit_testing
def test_dni_value_object_empty_value() -> None:
    """
    Test DniValueObject value object raises ValueError when value is empty.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'DniValueObject value <<<.*>>> is an empty string. Only non-empty strings are allowed.',
    ):
        DniValueObject(value=StringMother.empty())


@mark.unit_testing
def test_dni_value_object_not_trimmed_value() -> None:
    """
    Test DniValueObject value object raises ValueError when value is not trimmed.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'DniValueObject value <<<.*>>> contains leading or trailing whitespaces. Only trimmed values are allowed.',  # noqa: E501
    ):
        DniValueObject(value=f' {DniMother.create()} ')


@mark.unit_testing
def test_dni_value_object_invalid_value() -> None:
    """
    Test DniValueObject value object raises ValueError when value is not a valid dni.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'DniValueObject value <<<.*>>> is not a valid Spanish DNI.',
    ):
        DniValueObject(value=StringMother.create())


@mark.unit_testing
def test_dni_value_object_invalid_dni_letter() -> None:
    """
    Test DniValueObject value object raises ValueError when value is not a valid dni letter.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'DniValueObject value <<<87654321T>>> is not a valid Spanish DNI.',
    ):
        DniValueObject(value='87654321T')


@mark.unit_testing
def test_dni_value_object_invalid_processed_value() -> None:
    """
    Test DniValueObject defensive validation branch for invalid processed values.
    """
    dni_value: Any = DniValueObject(value='87654321-x')

    with assert_raises(
        expected_exception=ValueError,
        match=r'DniValueObject value <<<87654321X>>> is not a valid Spanish DNI.',
    ):
        dni_value._ensure_value_follows_validation_regex(value='87654321X', processed_value='INVALID')
