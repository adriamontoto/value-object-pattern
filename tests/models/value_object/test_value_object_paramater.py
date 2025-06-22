"""
Test value object module parameter attribute.
"""

from object_mother_pattern import StringMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables import TrimmedStringValueObject


@mark.unit_testing
def test_value_object_parameter_attribute_equals_default_value_object_name() -> None:
    """
    Test that a value object parameter attribute equals the default value object name if not provided.
    """
    value_object = TrimmedStringValueObject(value=StringMother.create())

    assert value_object.parameter == 'value'


@mark.unit_testing
def test_value_object_parameter_attribute_equals_custom_value_object_name() -> None:
    """
    Test that a value object parameter attribute equals the custom value object name.
    """
    parameter = StringMother.create()
    value_object = TrimmedStringValueObject(value=StringMother.create(), parameter=parameter)

    assert value_object.parameter == parameter


@mark.unit_testing
def test_value_object_parameter_attribute_accepts_empty_string() -> None:
    """
    Test that a value object parameter attribute accepts an empty string.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'ValueObject parameter <<<.*>>> must not be an empty string.',
    ):
        TrimmedStringValueObject(value=StringMother.create(), parameter=StringMother.empty())


@mark.unit_testing
def test_value_object_parameter_attribute_raises_type_error_when_not_string() -> None:
    """
    Test that a value object parameter attribute raises TypeError when not a string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'ValueObject parameter <<<.*>>> must be a string. Got <<<.*>>> instead.',
    ):
        TrimmedStringValueObject(value=StringMother.create(), parameter=StringMother.invalid_type())


@mark.unit_testing
def test_value_object_parameter_attribute_can_not_contain_leading_or_trailing_whitespaces() -> None:
    """
    Test that a value object parameter attribute can not contain leading or trailing whitespaces.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'ValueObject parameter <<<.*>>> contains leading or trailing whitespaces. Only trimmed values are allowed.',  # noqa: E501
    ):
        TrimmedStringValueObject(value=StringMother.create(), parameter=StringMother.not_trimmed())
