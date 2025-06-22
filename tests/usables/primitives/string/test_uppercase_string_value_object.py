"""
Test UppercaseStringValueObject value object.
"""

from object_mother_pattern import StringMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables import UppercaseStringValueObject


@mark.unit_testing
def test_uppercase_string_value_object_happy_path() -> None:
    """
    Test UppercaseStringValueObject value object happy path.
    """
    string_value = UppercaseStringValueObject(value=StringMother.uppercase())

    assert type(string_value.value) is str
    assert string_value.value.isupper()


@mark.unit_testing
def test_uppercase_string_value_object_invalid_value() -> None:
    """
    Test UppercaseStringValueObject value object raises ValueError when value is not uppercase.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'UppercaseStringValueObject value <<<.*>>> contains lowercase characters. Only uppercase characters are allowed.',  # noqa: E501
    ):
        UppercaseStringValueObject(value=StringMother.lowercase())


@mark.unit_testing
def test_uppercase_string_value_object_invalid_type() -> None:
    """
    Test UppercaseStringValueObject value object raises TypeError when value is not string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'StringValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        UppercaseStringValueObject(value=StringMother.invalid_type())
