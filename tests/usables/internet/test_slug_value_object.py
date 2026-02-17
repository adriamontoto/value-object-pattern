"""
Test SlugValueObject value object.
"""

from object_mother_pattern import StringMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.internet import SlugValueObject


# TODO: make it dynamic with object mother
@mark.unit_testing
def test_strict_string_identifier_value_object_happy_path() -> None:
    """
    Test SlugValueObject value object happy path.
    """
    identifier = SlugValueObject(value='abc-123-def')

    assert type(identifier.value) is str
    assert identifier.value == 'abc-123-def'


# TODO: make it dynamic with object mother
@mark.unit_testing
@mark.parametrize(argnames='value', argvalues=['abc_123', 'Abc-123', '-abc-123', 'abc--123', 'abc-123-'])
def test_strict_string_identifier_value_object_invalid_characters(value: str) -> None:
    """
    Test SlugValueObject value object raises ValueError when value has invalid format.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'SlugValueObject value <<<.*>>> has invalid format. Only lowercase letters and digits separated by single hyphens are allowed.',  # noqa: E501
    ):
        SlugValueObject(value=value)


@mark.unit_testing
def test_strict_string_identifier_value_object_empty_value() -> None:
    """
    Test SlugValueObject value object raises ValueError when value is empty.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'SlugValueObject value <<<.*>>> is an empty string. Only non-empty strings are allowed.',
    ):
        SlugValueObject(value=StringMother.empty())


@mark.unit_testing
def test_strict_string_identifier_value_object_not_trimmed() -> None:
    """
    Test SlugValueObject value object raises ValueError when value is not trimmed.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'SlugValueObject value <<<.*>>> contains leading or trailing whitespaces. Only trimmed values are allowed.',  # noqa: E501
    ):
        SlugValueObject(value=StringMother.not_trimmed())


@mark.unit_testing
def test_strict_string_identifier_value_object_invalid_type() -> None:
    """
    Test SlugValueObject value object raises TypeError when value is not a string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'SlugValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        SlugValueObject(value=StringMother.invalid_type())
