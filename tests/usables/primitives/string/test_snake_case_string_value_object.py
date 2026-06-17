"""
Test SnakeCaseStringValueObject value object.
"""

from object_mother_pattern import StringMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables import SnakeCaseStringValueObject


@mark.unit_testing
def test_snake_case_string_value_object_happy_path() -> None:
    """
    Test SnakeCaseStringValueObject value object happy path.
    """
    string_value = SnakeCaseStringValueObject(value='hello_world_123')

    assert type(string_value.value) is str
    assert string_value.value == 'hello_world_123'


@mark.unit_testing
def test_snake_case_string_value_object_invalid_value() -> None:
    """
    Test SnakeCaseStringValueObject value object raises ValueError when value is not snake_case.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'SnakeCaseStringValueObject value <<<.*>>> has invalid format. Only lowercase letters and digits separated by single underscores are allowed.',  # noqa: E501
    ):
        SnakeCaseStringValueObject(value='Hello_World')


@mark.unit_testing
def test_snake_case_string_value_object_empty_value() -> None:
    """
    Test SnakeCaseStringValueObject value object raises ValueError when value is an empty string.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'SnakeCaseStringValueObject value <<<.*>>> is an empty string. Only non-empty strings are allowed.',
    ):
        SnakeCaseStringValueObject(value=StringMother.empty())


@mark.unit_testing
def test_snake_case_string_value_object_not_trimmed() -> None:
    """
    Test SnakeCaseStringValueObject value object raises ValueError when value is not trimmed.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'SnakeCaseStringValueObject value <<<.*>>> contains leading or trailing whitespaces. Only trimmed values are allowed.',  # noqa: E501
    ):
        SnakeCaseStringValueObject(value=StringMother.not_trimmed())


@mark.unit_testing
def test_snake_case_string_value_object_invalid_type() -> None:
    """
    Test SnakeCaseStringValueObject value object raises TypeError when value is not a string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'SnakeCaseStringValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        SnakeCaseStringValueObject(value=StringMother.invalid_type())
