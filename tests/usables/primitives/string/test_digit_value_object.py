"""
Test DigitStringValueObject value object.
"""

from object_mother_pattern.mothers import IntegerMother, StringMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.primitives import DigitStringValueObject


@mark.unit_testing
def test_digit_string_value_object_happy_path() -> None:
    """
    Test DigitStringValueObject value object happy path.
    """
    string_value = DigitStringValueObject(value=str(object=IntegerMother.create()))

    assert type(string_value.value) is str
    assert string_value.value.isdigit()


@mark.unit_testing
def test_digit_string_value_object_invalid_value() -> None:
    """
    Test DigitStringValueObject value object raises ValueError when value contains non-digit characters.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'DigitStringValueObject value <<<.*>>> contains invalid characters. Only digit characters are allowed.',
    ):
        DigitStringValueObject(value=str(object=IntegerMother.invalid_type()))


@mark.unit_testing
def test_digit_string_value_object_invalid_type() -> None:
    """
    Test DigitStringValueObject value object raises TypeError when value is not string.
    """
    with assert_raises(
        expected_exception=TypeError, match=r'StringValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.'
    ):
        DigitStringValueObject(value=StringMother.invalid_type())
