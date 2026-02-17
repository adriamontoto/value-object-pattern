"""
Test KeyValueObject value object.
"""

from object_mother_pattern import StringMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.internet import KeyValueObject


# TODO: make it dynamic with object mother
@mark.unit_testing
def test_key_value_object_happy_path() -> None:
    """
    Test KeyValueObject value object happy path.
    """
    key = KeyValueObject(value='abc.123-def.ghi')

    assert type(key.value) is str
    assert key.value == 'abc.123-def.ghi'


# TODO: make it dynamic with object mother
@mark.unit_testing
@mark.parametrize(
    argnames='value',
    argvalues=['abc_123', 'Abc-123', '-abc.123', 'abc--123', 'abc..123', 'abc.-123', 'abc-.123', 'abc.123-'],
)
def test_key_value_object_invalid_characters(value: str) -> None:
    """
    Test KeyValueObject value object raises ValueError when value has invalid format.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'KeyValueObject value <<<.*>>> has invalid format. Only lowercase letters and digits separated by single hyphens or dots are allowed.',  # noqa: E501
    ):
        KeyValueObject(value=value)


@mark.unit_testing
def test_key_value_object_empty_value() -> None:
    """
    Test KeyValueObject value object raises ValueError when value is empty.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'KeyValueObject value <<<.*>>> is an empty string. Only non-empty strings are allowed.',
    ):
        KeyValueObject(value=StringMother.empty())


@mark.unit_testing
def test_key_value_object_not_trimmed() -> None:
    """
    Test KeyValueObject value object raises ValueError when value is not trimmed.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'KeyValueObject value <<<.*>>> contains leading or trailing whitespaces. Only trimmed values are allowed.',  # noqa: E501
    ):
        KeyValueObject(value=StringMother.not_trimmed())


@mark.unit_testing
def test_key_value_object_invalid_type() -> None:
    """
    Test KeyValueObject value object raises TypeError when value is not a string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'KeyValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        KeyValueObject(value=StringMother.invalid_type())
