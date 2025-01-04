"""
Test value object post validate process method.
"""

from sys import version_info

from object_mother_pattern.mothers import StringMother
from pytest import mark, raises as assert_raises

from value_object_pattern import ValueObject

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover


class UpperStringValueObject(ValueObject[str]):
    """
    UpperStringValueObject value object class.
    """

    @override
    def _post_validation_process(self, value: str) -> str:
        """
        Validate the value object.

        Args:
            value (int): Value object value.

        Returns:
            int: The value object value.
        """
        return value.upper()

    @override
    def _validate(self, value: str) -> None:
        """
        Validate the value object.

        Args:
            value (str): Value object value.

        Raises:
            TypeError: If the value object is not an string.
        """
        if type(value) is not str:
            raise TypeError(f'Value object must be a string, not {type(value).__name__}.')


@mark.unit_testing
def test_value_object_post_validate_process_method_happy_path() -> None:
    """
    Test value object post validate process method happy path, no validation errors.
    """
    string_value = StringMother.create().upper()
    _string = UpperStringValueObject(value=string_value)

    assert _string.value.isupper()


@mark.unit_testing
def test_value_object_post_validate_process_method_invalid_type() -> None:
    """
    Test value object post validate process method invalid type.
    """
    invalid_string = StringMother.invalid_type()

    with assert_raises(
        expected_exception=TypeError,
        match=f'Value object must be a string, not {type(invalid_string).__name__}.',
    ):
        UpperStringValueObject(value=invalid_string)
