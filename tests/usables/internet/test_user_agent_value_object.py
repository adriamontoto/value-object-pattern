"""
Test UserAgentValueObject value object.
"""

from object_mother_pattern import StringMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.internet import UserAgentValueObject


@mark.unit_testing
def test_user_agent_value_object_happy_path() -> None:
    """
    Test UserAgentValueObject value object happy path.
    """
    string_value = UserAgentValueObject(value='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15')

    assert type(string_value.value) is str
    assert string_value.value == 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15'


@mark.unit_testing
def test_user_agent_value_object_invalid_value() -> None:
    """
    Test UserAgentValueObject value object raises ValueError when value contains non-printable characters.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'UserAgentValueObject value <<<[\s\S]*>>> contains invalid characters. Only printable characters are allowed.',  # noqa: E501
    ):
        UserAgentValueObject(value='Mozilla/5.0\nSafari/605.1.15')


@mark.unit_testing
def test_user_agent_value_object_empty_value() -> None:
    """
    Test UserAgentValueObject value object raises ValueError when value is an empty string.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'UserAgentValueObject value <<<.*>>> is an empty string. Only non-empty strings are allowed.',
    ):
        UserAgentValueObject(value=StringMother.empty())


@mark.unit_testing
def test_user_agent_value_object_not_trimmed() -> None:
    """
    Test UserAgentValueObject value object raises ValueError when value is not trimmed.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'UserAgentValueObject value <<<.*>>> contains leading or trailing whitespaces. Only trimmed values are allowed.',  # noqa: E501
    ):
        UserAgentValueObject(value=StringMother.not_trimmed())


@mark.unit_testing
def test_user_agent_value_object_invalid_type() -> None:
    """
    Test UserAgentValueObject value object raises TypeError when value is not a string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'UserAgentValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        UserAgentValueObject(value=StringMother.invalid_type())
