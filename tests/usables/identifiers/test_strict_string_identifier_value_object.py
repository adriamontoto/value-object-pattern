"""
Test StrictStringIdentifierValueObject value object.
"""

from object_mother_pattern import StringMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.identifiers import StrictStringIdentifierValueObject


# TODO: make it dynamic with object mother
@mark.unit_testing
def test_strict_string_identifier_value_object_happy_path() -> None:
    """
    Test StrictStringIdentifierValueObject value object happy path.
    """
    identifier = StrictStringIdentifierValueObject(value='abc-123-def')

    assert type(identifier.value) is str
    assert identifier.value == 'abc-123-def'


# TODO: make it dynamic with object mother
@mark.unit_testing
@mark.parametrize(argnames='value', argvalues=['abc_123', 'Abc-123'])
def test_strict_string_identifier_value_object_invalid_characters(value: str) -> None:
    """
    Test StrictStringIdentifierValueObject value object raises ValueError when value has invalid characters.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StrictStringIdentifierValueObject value <<<.*>>> contains invalid characters. Only a-z, 0-9, and - are allowed.',  # noqa: E501
    ):
        StrictStringIdentifierValueObject(value=value)


@mark.unit_testing
def test_strict_string_identifier_value_object_empty_value() -> None:
    """
    Test StrictStringIdentifierValueObject value object raises ValueError when value is empty.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StrictStringIdentifierValueObject value <<<.*>>> is an empty string. Only non-empty strings are '
        r'allowed.',
    ):
        StrictStringIdentifierValueObject(value=StringMother.empty())


@mark.unit_testing
def test_strict_string_identifier_value_object_not_trimmed() -> None:
    """
    Test StrictStringIdentifierValueObject value object raises ValueError when value is not trimmed.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StrictStringIdentifierValueObject value <<<.*>>> contains leading or trailing whitespaces. Only trimmed values are allowed.',  # noqa: E501
    ):
        StrictStringIdentifierValueObject(value=StringMother.not_trimmed())


@mark.unit_testing
def test_strict_string_identifier_value_object_invalid_type() -> None:
    """
    Test StrictStringIdentifierValueObject value object raises TypeError when value is not a string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'StrictStringIdentifierValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        StrictStringIdentifierValueObject(value=StringMother.invalid_type())
