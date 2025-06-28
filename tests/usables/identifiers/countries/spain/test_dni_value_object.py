"""
Test DniValueObject value object.
"""

from object_mother_pattern import StringMother
from object_mother_pattern.mothers.identifiers.countries.spain import DniMother
from object_mother_pattern.mothers.primitives.utils.alphabets import ALPHABET_UPPERCASE_BASIC
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.identifiers.countries.spain import DniValueObject


@mark.unit_testing
def test_dni_value_object_happy_path() -> None:
    """
    Test DniValueObject value object happy path.
    """
    dni_value = DniValueObject(value=DniMother.create())

    assert type(dni_value.value) is str
    assert dni_value.value.isupper()


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
    dni_value = DniMother.create()
    last_letter = dni_value[-1].upper()

    dni_value = dni_value[:-1] + ALPHABET_UPPERCASE_BASIC.replace(last_letter, '', 1)

    with assert_raises(
        expected_exception=ValueError,
        match=r'DniValueObject value <<<.*>>> is not a valid Spanish DNI.',
    ):
        DniValueObject(value=dni_value)
