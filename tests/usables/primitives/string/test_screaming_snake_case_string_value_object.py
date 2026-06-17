"""
Test ScreamingSnakeCaseStringValueObject value object.
"""

from object_mother_pattern import StringMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables import ScreamingSnakeCaseStringValueObject


@mark.unit_testing
def test_screaming_snake_case_string_value_object_happy_path() -> None:
    """
    Test ScreamingSnakeCaseStringValueObject value object happy path.
    """
    string_value = ScreamingSnakeCaseStringValueObject(value='HELLO_WORLD_123')

    assert type(string_value.value) is str
    assert string_value.value == 'HELLO_WORLD_123'


@mark.unit_testing
def test_screaming_snake_case_string_value_object_invalid_value() -> None:
    """
    Test ScreamingSnakeCaseStringValueObject value object raises ValueError when value is not SCREAMING_SNAKE_CASE.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'ScreamingSnakeCaseStringValueObject value <<<.*>>> has invalid format. Only uppercase letters and digits separated by single underscores are allowed.',  # noqa: E501
    ):
        ScreamingSnakeCaseStringValueObject(value='Hello_WORLD')


@mark.unit_testing
def test_screaming_snake_case_string_value_object_empty_value() -> None:
    """
    Test ScreamingSnakeCaseStringValueObject value object raises ValueError when value is an empty string.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=(
            r'ScreamingSnakeCaseStringValueObject value <<<.*>>> is an empty string. '
            r'Only non-empty strings are allowed.'
        ),
    ):
        ScreamingSnakeCaseStringValueObject(value=StringMother.empty())


@mark.unit_testing
def test_screaming_snake_case_string_value_object_not_trimmed() -> None:
    """
    Test ScreamingSnakeCaseStringValueObject value object raises ValueError when value is not trimmed.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'ScreamingSnakeCaseStringValueObject value <<<.*>>> contains leading or trailing whitespaces. Only trimmed values are allowed.',  # noqa: E501
    ):
        ScreamingSnakeCaseStringValueObject(value=StringMother.not_trimmed())


@mark.unit_testing
def test_screaming_snake_case_string_value_object_invalid_type() -> None:
    """
    Test ScreamingSnakeCaseStringValueObject value object raises TypeError when value is not a string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'ScreamingSnakeCaseStringValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        ScreamingSnakeCaseStringValueObject(value=StringMother.invalid_type())
