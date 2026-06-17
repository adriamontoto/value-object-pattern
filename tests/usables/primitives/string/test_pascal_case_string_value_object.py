"""
Test PascalCaseStringValueObject value object.
"""

from object_mother_pattern import StringMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables import PascalCaseStringValueObject


@mark.unit_testing
def test_pascal_case_string_value_object_happy_path() -> None:
    """
    Test PascalCaseStringValueObject value object happy path.
    """
    string_value = PascalCaseStringValueObject(value='HelloWorld123')

    assert type(string_value.value) is str
    assert string_value.value == 'HelloWorld123'


@mark.unit_testing
def test_pascal_case_string_value_object_invalid_value() -> None:
    """
    Test PascalCaseStringValueObject value object raises ValueError when value is not PascalCase.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'PascalCaseStringValueObject value <<<.*>>> has invalid format. Only PascalCase strings starting with an uppercase letter and continuing with alphanumeric words are allowed.',  # noqa: E501
    ):
        PascalCaseStringValueObject(value='helloWorld')


@mark.unit_testing
def test_pascal_case_string_value_object_empty_value() -> None:
    """
    Test PascalCaseStringValueObject value object raises ValueError when value is an empty string.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'PascalCaseStringValueObject value <<<.*>>> is an empty string. Only non-empty strings are allowed.',
    ):
        PascalCaseStringValueObject(value=StringMother.empty())


@mark.unit_testing
def test_pascal_case_string_value_object_not_trimmed() -> None:
    """
    Test PascalCaseStringValueObject value object raises ValueError when value is not trimmed.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'PascalCaseStringValueObject value <<<.*>>> contains leading or trailing whitespaces. Only trimmed values are allowed.',  # noqa: E501
    ):
        PascalCaseStringValueObject(value=StringMother.not_trimmed())


@mark.unit_testing
def test_pascal_case_string_value_object_invalid_type() -> None:
    """
    Test PascalCaseStringValueObject value object raises TypeError when value is not a string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'PascalCaseStringValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        PascalCaseStringValueObject(value=StringMother.invalid_type())
