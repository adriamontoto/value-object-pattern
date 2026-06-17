"""
Test SnakeCaseKeyValueObject value object.
"""

from object_mother_pattern import StringMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.internet.keys import SnakeCaseKeyValueObject


@mark.unit_testing
def test_snake_case_key_value_object_happy_path() -> None:
    """
    Test SnakeCaseKeyValueObject value object happy path.
    """
    key = SnakeCaseKeyValueObject(value='organization.api_keys')

    assert type(key.value) is str
    assert key.value == 'organization.api_keys'


@mark.unit_testing
def test_snake_case_key_value_object_invalid_uppercase_letter() -> None:
    """
    Test SnakeCaseKeyValueObject value object raises ValueError when value has invalid format.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'SnakeCaseKeyValueObject value <<<.*>>> has invalid format. Only lowercase letters and digits separated by single underscores inside dot-separated segments are allowed.',  # noqa: E501
    ):
        SnakeCaseKeyValueObject(value='Organization.api_keys')


@mark.unit_testing
def test_snake_case_key_value_object_invalid_hyphenated_segment() -> None:
    """
    Test SnakeCaseKeyValueObject value object raises ValueError when value has invalid format.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'SnakeCaseKeyValueObject value <<<.*>>> has invalid format. Only lowercase letters and digits separated by single underscores inside dot-separated segments are allowed.',  # noqa: E501
    ):
        SnakeCaseKeyValueObject(value='organization.api-keys')


@mark.unit_testing
def test_snake_case_key_value_object_invalid_empty_segment() -> None:
    """
    Test SnakeCaseKeyValueObject value object raises ValueError when value has invalid format.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'SnakeCaseKeyValueObject value <<<.*>>> has invalid format. Only lowercase letters and digits separated by single underscores inside dot-separated segments are allowed.',  # noqa: E501
    ):
        SnakeCaseKeyValueObject(value='organization..api_keys')


@mark.unit_testing
def test_snake_case_key_value_object_invalid_leading_dot() -> None:
    """
    Test SnakeCaseKeyValueObject value object raises ValueError when value has invalid format.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'SnakeCaseKeyValueObject value <<<.*>>> has invalid format. Only lowercase letters and digits separated by single underscores inside dot-separated segments are allowed.',  # noqa: E501
    ):
        SnakeCaseKeyValueObject(value='.organization.api_keys')


@mark.unit_testing
def test_snake_case_key_value_object_empty_value() -> None:
    """
    Test SnakeCaseKeyValueObject value object raises ValueError when value is empty.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'SnakeCaseKeyValueObject value <<<.*>>> is an empty string. Only non-empty strings are allowed.',
    ):
        SnakeCaseKeyValueObject(value=StringMother.empty())


@mark.unit_testing
def test_snake_case_key_value_object_not_trimmed() -> None:
    """
    Test SnakeCaseKeyValueObject value object raises ValueError when value is not trimmed.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'SnakeCaseKeyValueObject value <<<.*>>> contains leading or trailing whitespaces. Only trimmed values are allowed.',  # noqa: E501
    ):
        SnakeCaseKeyValueObject(value=StringMother.not_trimmed())


@mark.unit_testing
def test_snake_case_key_value_object_invalid_type() -> None:
    """
    Test SnakeCaseKeyValueObject value object raises TypeError when value is not a string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'SnakeCaseKeyValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        SnakeCaseKeyValueObject(value=StringMother.invalid_type())
