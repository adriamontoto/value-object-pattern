"""
Test AlphabeticStringValueObject value object.
"""

from object_mother_pattern.mothers import IntegerMother, StringMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.primitives import AlphabeticStringValueObject


@mark.unit_testing
def test_alphabetic_string_value_object_happy_path() -> None:
    """
    Test AlphabeticStringValueObject value object happy path.
    """
    string_value = AlphabeticStringValueObject(value=StringMother.create())

    assert type(string_value.value) is str
    assert string_value.value.isalpha()


@mark.unit_testing
def test_alphabetic_string_value_object_invalid_value() -> None:
    """
    Test AlphabeticStringValueObject value object raises ValueError when value contains not alphabetic characters.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'AlphabeticStringValueObject value <<<.*>>> contains invalid characters. Only alphabetic characters are allowed.',  # noqa: E501
    ):
        AlphabeticStringValueObject(value=f'{StringMother.create()}{IntegerMother.create()}')


@mark.unit_testing
def test_alphabetic_string_value_object_invalid_type() -> None:
    """
    Test AlphabeticStringValueObject value object raises TypeError when value is not string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'StringValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        AlphabeticStringValueObject(value=StringMother.invalid_type())
