"""
Test NotEmptyStringValueObject value object.
"""

from object_mother_pattern.mothers import StringMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.primitives import NotEmptyStringValueObject


@mark.unit_testing
def test_not_empty_string_value_object_happy_path() -> None:
    """
    Test NotEmptyStringValueObject value object happy path.
    """
    string_value = NotEmptyStringValueObject(value=StringMother.create())

    assert type(string_value.value) is str
    assert string_value.value != ''


@mark.unit_testing
def test_not_empty_string_value_object_invalid_value() -> None:
    """
    Test NotEmptyStringValueObject value object raises ValueError when value is an empty string.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'NotEmptyStringValueObject value <<<.*>>> is an empty string. Only non-empty strings are allowed.',
    ):
        NotEmptyStringValueObject(value='')


@mark.unit_testing
def test_not_empty_string_value_object_invalid_type() -> None:
    """
    Test NotEmptyStringValueObject value object raises TypeError when value is not string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'StringValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        NotEmptyStringValueObject(value=StringMother.invalid_type())
