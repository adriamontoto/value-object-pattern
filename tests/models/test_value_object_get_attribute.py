"""
Test value object module.
"""

from object_mother_pattern.mothers import IntegerMother
from pytest import mark, raises as assert_raises

from value_object_pattern import ValueObject


class IntegerValueObject(ValueObject[int]):
    """
    IntegerValueObject value object class.
    """


@mark.unit_testing
def test_value_object_get_attribute() -> None:
    """
    Test that a value object value can be accessed.
    """
    value_object = IntegerValueObject(value=IntegerMother.create())

    value_object.value  # noqa: B018


@mark.unit_testing
def test_value_object_get_protected_attribute() -> None:
    """
    Test that a value object protected value can be accessed.
    """
    value_object = IntegerValueObject(value=IntegerMother.create())

    value_object._value  # noqa: B018


@mark.unit_testing
def test_value_object_cannot_get_unexistent_attribute() -> None:
    """
    Test that a value object value cannot be modified after initialization.
    """
    value_object = IntegerValueObject(value=IntegerMother.create())

    with assert_raises(
        expected_exception=AttributeError,
        match=f"'{value_object.__class__.__name__}' object has no attribute 'not_existent_attribute'",
    ):
        value_object.not_existent_attribute  # type: ignore[attr-defined]  # noqa: B018
