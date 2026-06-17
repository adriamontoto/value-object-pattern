"""
Test ListValueObject display value branches.
"""

from enum import Enum
from typing import Any

from pytest import mark

from value_object_pattern import ValueObject
from value_object_pattern.models.collections import ListValueObject


class DisplayColor(Enum):
    """
    Colors used by list value object display tests.
    """

    RED = 'red'


class DisplayColorValueObject(ValueObject[DisplayColor]):
    """
    Value object wrapping an enum.
    """


class DisplayColorValueObjectList(ListValueObject[DisplayColorValueObject]):
    """
    List value object wrapping enum value objects.
    """


class AnyDisplayListValueObject(ListValueObject[Any]):
    """
    List value object that accepts plain helper objects.
    """


class DisplayColorValueAttribute:
    """
    Plain object whose value attribute stores an enum.
    """

    value: DisplayColor

    def __init__(self) -> None:
        """
        Initialize the enum value attribute.
        """
        self.value = DisplayColor.RED


class NumberValueAttribute:
    """
    Plain object whose value attribute stores a non-enum primitive.
    """

    value: int

    def __init__(self) -> None:
        """
        Initialize the primitive value attribute.
        """
        self.value = 42


@mark.unit_testing
def test_list_value_object_repr_handles_enum_display_values_inside_value_objects() -> None:
    """
    Test ListValueObject repr handles ValueObjects wrapping Enum values.
    """
    sequence = DisplayColorValueObjectList(value=[DisplayColorValueObject(value=DisplayColor.RED)])

    assert repr(sequence) == '["\'red\'"]'


@mark.unit_testing
def test_list_value_object_str_handles_enum_display_values_inside_value_objects() -> None:
    """
    Test ListValueObject str handles ValueObjects wrapping Enum values.
    """
    sequence = DisplayColorValueObjectList(value=[DisplayColorValueObject(value=DisplayColor.RED)])

    assert str(sequence) == "['red']"


@mark.unit_testing
def test_list_value_object_repr_handles_enum_value_attributes() -> None:
    """
    Test ListValueObject repr handles objects whose value attribute stores an Enum.
    """
    sequence = AnyDisplayListValueObject(value=[DisplayColorValueAttribute()])

    assert repr(sequence) == '["\'red\'"]'


@mark.unit_testing
def test_list_value_object_str_handles_enum_value_attributes() -> None:
    """
    Test ListValueObject str handles objects whose value attribute stores an Enum.
    """
    sequence = AnyDisplayListValueObject(value=[DisplayColorValueAttribute()])

    assert str(sequence) == "['red']"


@mark.unit_testing
def test_list_value_object_repr_handles_primitive_value_attributes() -> None:
    """
    Test ListValueObject repr handles objects whose value attribute stores a primitive.
    """
    sequence = AnyDisplayListValueObject(value=[NumberValueAttribute()])

    assert repr(sequence) == "['42']"


@mark.unit_testing
def test_list_value_object_str_handles_primitive_value_attributes() -> None:
    """
    Test ListValueObject str handles objects whose value attribute stores a primitive.
    """
    sequence = AnyDisplayListValueObject(value=[NumberValueAttribute()])

    assert str(sequence) == "['42']"
