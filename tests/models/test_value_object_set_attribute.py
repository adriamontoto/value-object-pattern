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
def test_value_object_cannot_modify_value() -> None:
    """
    Test that a value object value cannot be modified after initialization.
    """
    value_object = IntegerValueObject(value=IntegerMother.create())

    with assert_raises(
        expected_exception=AttributeError,
        match='Cannot modify attribute "value" of immutable instance',
    ):
        value_object.value = IntegerMother.create()  # type: ignore[misc]


@mark.unit_testing
def test_value_object_cannot_modify_protected_value() -> None:
    """
    Test that a value object protected value cannot be modified after initialization.
    """
    value_object = IntegerValueObject(value=IntegerMother.create())

    with assert_raises(
        expected_exception=AttributeError,
        match='Cannot modify attribute "_value" of immutable instance',
    ):
        value_object._value = IntegerMother.create()


@mark.unit_testing
def test_value_object_cannot_add_new_attribute() -> None:
    """
    Test that cannot add a new attribute to a value object after initialization.
    """
    value_object = IntegerValueObject(value=IntegerMother.create())

    with assert_raises(
        expected_exception=AttributeError,
        match=f'{value_object.__class__.__name__} object has no attribute "new_attribute"',
    ):
        value_object.new_attribute = IntegerMother.create()
