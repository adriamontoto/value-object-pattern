"""
Test TrimmedStringValueObject value object.
"""

from object_mother_pattern.mothers import StringMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.primitives import TrimmedStringValueObject


@mark.unit_testing
def test_trimmed_string_value_object_happy_path() -> None:
    """
    Test TrimmedStringValueObject value object happy path.
    """
    string_value = TrimmedStringValueObject(value=StringMother.create())

    assert type(string_value.value) is str
    assert string_value.value == string_value.value.strip()


@mark.unit_testing
def test_trimmed_string_value_object_invalid_value() -> None:
    """
    Test TrimmedStringValueObject value object raises ValueError when value contains leading or trailing whitespaces.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'TrimmedStringValueObject value <<<.*>>> contains leading or trailing whitespaces. Only trimmed values are allowed.',  # noqa: E501
    ):
        TrimmedStringValueObject(value=f'  {StringMother.create()}  ')


@mark.unit_testing
def test_trimmed_string_value_object_invalid_type() -> None:
    """
    Test TrimmedStringValueObject value object raises TypeError when value is not string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'StringValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        TrimmedStringValueObject(value=StringMother.invalid_type())
