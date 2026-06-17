"""
Test KebabCaseStringValueObject value object.
"""

from object_mother_pattern import StringMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables import KebabCaseStringValueObject


@mark.unit_testing
def test_kebab_case_string_value_object_happy_path() -> None:
    """
    Test KebabCaseStringValueObject value object happy path.
    """
    string_value = KebabCaseStringValueObject(value='hello-world-123')

    assert type(string_value.value) is str
    assert string_value.value == 'hello-world-123'


@mark.unit_testing
def test_kebab_case_string_value_object_invalid_value() -> None:
    """
    Test KebabCaseStringValueObject value object raises ValueError when value is not kebab-case.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'KebabCaseStringValueObject value <<<.*>>> has invalid format. Only lowercase letters and digits separated by single hyphens are allowed.',  # noqa: E501
    ):
        KebabCaseStringValueObject(value='Hello-World')


@mark.unit_testing
def test_kebab_case_string_value_object_empty_value() -> None:
    """
    Test KebabCaseStringValueObject value object raises ValueError when value is an empty string.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'KebabCaseStringValueObject value <<<.*>>> is an empty string. Only non-empty strings are allowed.',
    ):
        KebabCaseStringValueObject(value=StringMother.empty())


@mark.unit_testing
def test_kebab_case_string_value_object_not_trimmed() -> None:
    """
    Test KebabCaseStringValueObject value object raises ValueError when value is not trimmed.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'KebabCaseStringValueObject value <<<.*>>> contains leading or trailing whitespaces. Only trimmed values are allowed.',  # noqa: E501
    ):
        KebabCaseStringValueObject(value=StringMother.not_trimmed())


@mark.unit_testing
def test_kebab_case_string_value_object_invalid_type() -> None:
    """
    Test KebabCaseStringValueObject value object raises TypeError when value is not a string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'KebabCaseStringValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        KebabCaseStringValueObject(value=StringMother.invalid_type())
