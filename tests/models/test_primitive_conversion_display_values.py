"""
Test primitive conversion display value branches.
"""

from __future__ import annotations

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from enum import Enum
from typing import Any

from pytest import mark

from value_object_pattern import ValueObject
from value_object_pattern.models.primitive_conversion import to_primitive


class DisplayColor(Enum):
    """
    Colors used by value object display tests.
    """

    RED = 'red'


class SelfDisplayingValueObject(ValueObject[str]):
    """
    Value object whose display value intentionally points to itself.
    """

    @override
    def _value_for_display(self) -> Any:
        """
        Return self to cover recursive primitive fallback.
        """
        return self

    @override
    def __str__(self) -> str:
        """
        Return a stable display string even though _value_for_display returns self.
        """
        return 'self-display'


class SelfValueAttribute:
    """
    Plain object whose value attribute points to itself.
    """

    value: SelfValueAttribute

    def __init__(self) -> None:
        """
        Initialize the self-referential value attribute.
        """
        self.value = self

    @override
    def __str__(self) -> str:
        """
        Return a stable string representation.
        """
        return 'self-value'


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


@mark.unit_testing
def test_to_primitive_returns_string_when_value_object_display_value_points_to_self() -> None:
    """
    Test primitive conversion fallback when a value object display value points to itself.
    """
    assert to_primitive(value=SelfDisplayingValueObject(value='visible')) == 'self-display'


@mark.unit_testing
def test_to_primitive_returns_string_when_value_attribute_points_to_self() -> None:
    """
    Test primitive conversion fallback when a value attribute points to itself.
    """
    assert to_primitive(value=SelfValueAttribute()) == 'self-value'


@mark.unit_testing
def test_to_primitive_converts_enum_value_attributes() -> None:
    """
    Test primitive conversion unwraps value attributes that store Enum values.
    """
    assert to_primitive(value=DisplayColorValueAttribute()) == 'red'
