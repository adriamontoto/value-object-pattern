"""
Test value object validate method.
"""

from sys import version_info

from object_mother_pattern.mothers import IntegerMother
from pytest import mark, raises as assert_raises

from value_object_pattern import ValueObject

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover


class NaturalValueObject(ValueObject[int]):
    """
    NaturalValueObject value object class.
    """

    @override
    def _validate(self, value: int) -> None:
        """
        Validate the value object.

        Args:
            value (int): Value object value.

        Raises:
            TypeError: If the value object is not an integer.
            ValueError: If the value object is not a natural number.
        """
        if type(value) is not int:
            raise TypeError(f'Value object must be an integer, not {type(value).__name__}.')

        if value <= 0:
            raise ValueError('Value object must be a natural number.')


@mark.unit_testing
def test_value_object_validate_method_happy_path() -> None:
    """
    Test value object validate method happy path, no validation errors.
    """
    natural_value = IntegerMother.positive()
    NaturalValueObject(value=natural_value)


@mark.unit_testing
def test_value_object_validate_method_invalid_type() -> None:
    """
    Test value object validate method invalid type.
    """
    invalid_natural = IntegerMother.invalid_type()

    with assert_raises(
        expected_exception=TypeError,
        match=f'Value object must be an integer, not {type(invalid_natural).__name__}.',
    ):
        NaturalValueObject(value=invalid_natural)


@mark.unit_testing
def test_value_object_validate_method_invalid_value() -> None:
    """
    Test value object validate method invalid value.
    """
    invalid_natural = IntegerMother.create(min=-100, max=0)

    with assert_raises(
        expected_exception=ValueError,
        match='Value object must be a natural number.',
    ):
        NaturalValueObject(value=invalid_natural)
