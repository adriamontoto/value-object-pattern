"""
Test AlphanumericStringValueObject value object.
"""

from object_mother_pattern import StringMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables import AlphanumericStringValueObject


@mark.unit_testing
def test_alphanumeric_string_value_object_happy_path() -> None:
    """
    Test AlphanumericStringValueObject value object happy path.
    """
    string_value = AlphanumericStringValueObject(value=StringMother.alphanumeric())

    assert type(string_value.value) is str
    assert string_value.value.isalnum()


@mark.unit_testing
def test_alphanumeric_string_value_object_invalid_value() -> None:
    """
    Test AlphanumericStringValueObject value object raises ValueError when value contains not alphanumeric characters.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'AlphanumericStringValueObject value <<<.*>>> contains invalid characters. Only alphanumeric characters are allowed.',  # noqa: E501
    ):
        AlphanumericStringValueObject(value=StringMother.invalid_value())


@mark.unit_testing
def test_alphanumeric_string_value_object_invalid_type() -> None:
    """
    Test AlphanumericStringValueObject value object raises TypeError when value is not string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'StringValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        AlphanumericStringValueObject(value=StringMother.invalid_type())
