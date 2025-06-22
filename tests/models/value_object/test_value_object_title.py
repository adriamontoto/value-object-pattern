"""
Test value object module title attribute.
"""

from object_mother_pattern import StringMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables import TrimmedStringValueObject


@mark.unit_testing
def test_value_object_title_attribute_equals_default_value_object_name() -> None:
    """
    Test that a value object title attribute equals the default value object name if not provided.
    """
    value_object = TrimmedStringValueObject(value=StringMother.create())

    assert value_object.title == 'TrimmedStringValueObject'


@mark.unit_testing
def test_value_object_title_attribute_equals_custom_value_object_name() -> None:
    """
    Test that a value object title attribute equals the custom value object name.
    """
    title_name = StringMother.create()
    value_object = TrimmedStringValueObject(value=StringMother.create(), title=title_name)

    assert value_object.title == title_name


@mark.unit_testing
def test_value_object_title_attribute_raises_value_error_when_empty_string() -> None:
    """
    Test that a value object title attribute raises ValueError when an empty string is provided.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'ValueObject title <<<.*>>> must not be an empty string.',
    ):
        TrimmedStringValueObject(value=StringMother.create(), title=StringMother.empty())


@mark.unit_testing
def test_value_object_title_attribute_raises_type_error_when_not_string() -> None:
    """
    Test that a value object title attribute raises TypeError when not a string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'ValueObject title <<<.*>>> must be a string. Got <<<.*>>> instead.',
    ):
        TrimmedStringValueObject(value=StringMother.create(), title=StringMother.invalid_type())


@mark.unit_testing
def test_value_object_title_attribute_can_not_contain_leading_or_trailing_whitespaces() -> None:
    """
    Test that a value object title attribute can not contain leading or trailing whitespaces.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'ValueObject title <<<.*>>> contains leading or trailing whitespaces. Only trimmed values are allowed.',
    ):
        TrimmedStringValueObject(value=StringMother.create(), title=StringMother.not_trimmed())
