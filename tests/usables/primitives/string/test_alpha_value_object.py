"""
Test AlphaStringValueObject value object.
"""

from object_mother_pattern import StringMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables import AlphaStringValueObject


@mark.unit_testing
def test_alpha_string_value_object_happy_path() -> None:
    """
    Test AlphaStringValueObject value object happy path.
    """
    string_value = AlphaStringValueObject(value=StringMother.alpha())

    assert type(string_value.value) is str
    assert string_value.value.isalpha()


@mark.unit_testing
def test_alpha_string_value_object_invalid_value() -> None:
    """
    Test AlphaStringValueObject value object raises ValueError when value contains not alpha characters.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'AlphaStringValueObject value <<<.*>>> contains invalid characters. Only alpha characters are allowed.',  # noqa: E501
    ):
        AlphaStringValueObject(value=StringMother.numeric())


@mark.unit_testing
def test_alpha_string_value_object_invalid_type() -> None:
    """
    Test AlphaStringValueObject value object raises TypeError when value is not string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'StringValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        AlphaStringValueObject(value=StringMother.invalid_type())
