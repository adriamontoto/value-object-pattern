"""
Test classproperty decorator.
"""

from object_mother_pattern.models import BaseMother
from pytest import mark, raises as assert_raises

from value_object_pattern.decorators import classproperty


class ClassPropertySample:
    """
    Class used to test the classproperty decorator.
    """

    prefix = 'hello'

    @classproperty
    def greeting(cls) -> str:  # noqa: N805
        """Classproperty docstring."""
        return cls.prefix.upper()


@mark.unit_testing
def test_classproperty_returns_same_value_for_class() -> None:
    """
    Test that a classproperty returns the same value from the class.
    """
    assert ClassPropertySample.greeting == 'HELLO'


@mark.unit_testing
def test_classproperty_returns_same_value_for_instance() -> None:
    """
    Test that a classproperty returns the same value from the its instances.
    """
    assert ClassPropertySample().greeting == 'HELLO'


@mark.unit_testing
def test_classproperty_preserves_docstring() -> None:
    """
    Test that a classproperty copies the wrapped function docstring.
    """
    descriptor = ClassPropertySample.__dict__['greeting']

    assert descriptor.__doc__ == 'Classproperty docstring.'


@mark.unit_testing
def test_classproperty_raises_type_error_when_not_callable() -> None:
    """
    Test that classproperty raises a TypeError when wrapping a non-callable object.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'Wrapped function must be callable\. Got <<<.*>>> instead\.',
    ):
        classproperty(function=BaseMother.invalid_type())
