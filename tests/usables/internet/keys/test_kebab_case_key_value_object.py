"""
Test KebabCaseKeyValueObject value object.
"""

from object_mother_pattern import StringMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.internet.keys import KebabCaseKeyValueObject


@mark.unit_testing
def test_kebab_case_key_value_object_happy_path() -> None:
    """
    Test KebabCaseKeyValueObject value object happy path.
    """
    key = KebabCaseKeyValueObject(value='organization.api-keys')

    assert type(key.value) is str
    assert key.value == 'organization.api-keys'


@mark.unit_testing
def test_kebab_case_key_value_object_invalid_uppercase_letter() -> None:
    """
    Test KebabCaseKeyValueObject value object raises ValueError when value has invalid format.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'KebabCaseKeyValueObject value <<<.*>>> has invalid format. Only lowercase letters and digits separated by single hyphens inside dot-separated segments are allowed.',  # noqa: E501
    ):
        KebabCaseKeyValueObject(value='Organization.api-keys')


@mark.unit_testing
def test_kebab_case_key_value_object_invalid_snake_case_segment() -> None:
    """
    Test KebabCaseKeyValueObject value object raises ValueError when value has invalid format.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'KebabCaseKeyValueObject value <<<.*>>> has invalid format. Only lowercase letters and digits separated by single hyphens inside dot-separated segments are allowed.',  # noqa: E501
    ):
        KebabCaseKeyValueObject(value='organization.api_keys')


@mark.unit_testing
def test_kebab_case_key_value_object_invalid_empty_segment() -> None:
    """
    Test KebabCaseKeyValueObject value object raises ValueError when value has invalid format.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'KebabCaseKeyValueObject value <<<.*>>> has invalid format. Only lowercase letters and digits separated by single hyphens inside dot-separated segments are allowed.',  # noqa: E501
    ):
        KebabCaseKeyValueObject(value='organization..api-keys')


@mark.unit_testing
def test_kebab_case_key_value_object_invalid_leading_dot() -> None:
    """
    Test KebabCaseKeyValueObject value object raises ValueError when value has invalid format.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'KebabCaseKeyValueObject value <<<.*>>> has invalid format. Only lowercase letters and digits separated by single hyphens inside dot-separated segments are allowed.',  # noqa: E501
    ):
        KebabCaseKeyValueObject(value='.organization.api-keys')


@mark.unit_testing
def test_kebab_case_key_value_object_empty_value() -> None:
    """
    Test KebabCaseKeyValueObject value object raises ValueError when value is empty.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'KebabCaseKeyValueObject value <<<.*>>> is an empty string. Only non-empty strings are allowed.',
    ):
        KebabCaseKeyValueObject(value=StringMother.empty())


@mark.unit_testing
def test_kebab_case_key_value_object_not_trimmed() -> None:
    """
    Test KebabCaseKeyValueObject value object raises ValueError when value is not trimmed.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'KebabCaseKeyValueObject value <<<.*>>> contains leading or trailing whitespaces. Only trimmed values are allowed.',  # noqa: E501
    ):
        KebabCaseKeyValueObject(value=StringMother.not_trimmed())


@mark.unit_testing
def test_kebab_case_key_value_object_invalid_type() -> None:
    """
    Test KebabCaseKeyValueObject value object raises TypeError when value is not a string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'KebabCaseKeyValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        KebabCaseKeyValueObject(value=StringMother.invalid_type())
