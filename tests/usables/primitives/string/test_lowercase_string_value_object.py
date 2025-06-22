"""
Test LowercaseStringValueObject value object.
"""

from object_mother_pattern import StringMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables import LowercaseStringValueObject


@mark.unit_testing
def test_lowercase_string_value_object_happy_path() -> None:
    """
    Test LowercaseStringValueObject value object happy path.
    """
    string_value = LowercaseStringValueObject(value=StringMother.lowercase())

    assert type(string_value.value) is str
    assert string_value.value.islower()


@mark.unit_testing
def test_lowercase_string_value_object_invalid_value() -> None:
    """
    Test LowercaseStringValueObject value object raises ValueError when value is not lowercase.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'LowercaseStringValueObject value <<<.*>>> contains uppercase characters. Only lowercase characters are allowed.',  # noqa: E501
    ):
        LowercaseStringValueObject(value=StringMother.uppercase())


@mark.unit_testing
def test_lowercase_string_value_object_invalid_type() -> None:
    """
    Test LowercaseStringValueObject value object raises TypeError when value is not string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'StringValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        LowercaseStringValueObject(value=StringMother.invalid_type())
