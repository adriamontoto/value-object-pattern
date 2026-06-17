"""
Test CamelCaseStringValueObject value object.
"""

from object_mother_pattern import StringMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables import CamelCaseStringValueObject


@mark.unit_testing
def test_camel_case_string_value_object_happy_path() -> None:
    """
    Test CamelCaseStringValueObject value object happy path.
    """
    string_value = CamelCaseStringValueObject(value='helloWorld123')

    assert type(string_value.value) is str
    assert string_value.value == 'helloWorld123'


@mark.unit_testing
def test_camel_case_string_value_object_invalid_value() -> None:
    """
    Test CamelCaseStringValueObject value object raises ValueError when value is not camelCase.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'CamelCaseStringValueObject value <<<.*>>> has invalid format. Only camelCase strings starting with a lowercase letter and continuing with alphanumeric words are allowed.',  # noqa: E501
    ):
        CamelCaseStringValueObject(value='HelloWorld')


@mark.unit_testing
def test_camel_case_string_value_object_empty_value() -> None:
    """
    Test CamelCaseStringValueObject value object raises ValueError when value is an empty string.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'CamelCaseStringValueObject value <<<.*>>> is an empty string. Only non-empty strings are allowed.',
    ):
        CamelCaseStringValueObject(value=StringMother.empty())


@mark.unit_testing
def test_camel_case_string_value_object_not_trimmed() -> None:
    """
    Test CamelCaseStringValueObject value object raises ValueError when value is not trimmed.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'CamelCaseStringValueObject value <<<.*>>> contains leading or trailing whitespaces. Only trimmed values are allowed.',  # noqa: E501
    ):
        CamelCaseStringValueObject(value=StringMother.not_trimmed())


@mark.unit_testing
def test_camel_case_string_value_object_invalid_type() -> None:
    """
    Test CamelCaseStringValueObject value object raises TypeError when value is not a string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'CamelCaseStringValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        CamelCaseStringValueObject(value=StringMother.invalid_type())
