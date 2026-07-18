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
from value_object_pattern.models.primitive_conversion import to_display_primitive, to_primitive


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


class SelfToPrimitives:
    """
    Helper object whose to_primitives returns itself.
    """

    def to_primitives(self) -> SelfToPrimitives:
        """
        Return itself to exercise the display conversion guard.
        """
        return self

    @override
    def __str__(self) -> str:
        """
        Stable string representation.
        """
        return 'self-to-primitives'


class SelfValueObject(ValueObject[Any]):
    """
    Value object whose value points to itself.
    """

    def __init__(self) -> None:
        """
        Initialize with a self-referential value.
        """
        super().__init__(value=self)

    @override
    def __str__(self) -> str:
        """
        Return a stable string for the self-referential value.
        """
        return 'self-value-object'


@mark.unit_testing
def test_to_primitive_uses_raw_value_when_display_value_points_to_self() -> None:
    """
    Test primitive conversion ignores a self-referential display value.
    """
    assert to_primitive(value=SelfDisplayingValueObject(value='visible')) == 'visible'


@mark.unit_testing
def test_to_primitive_returns_string_when_value_object_value_points_to_self() -> None:
    """
    Test primitive conversion fallback when a value object's raw value points to itself.
    """
    assert to_primitive(value=SelfValueObject()) == 'self-value-object'


@mark.unit_testing
def test_to_display_primitive_returns_string_when_value_object_display_value_points_to_self() -> None:
    """
    Test display conversion fallback when a value object's display value points to itself.
    """
    assert to_display_primitive(value=SelfDisplayingValueObject(value='visible')) == 'self-display'


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


@mark.unit_testing
def test_to_display_primitive_recursively_converts_collections() -> None:
    """
    Test display conversion recursively handles supported collection types.
    """
    value = {
        'list': [DisplayColor.RED],
        'tuple': (DisplayColor.RED,),
        'set': {DisplayColor.RED},
        'frozenset': frozenset({DisplayColor.RED}),
    }

    assert to_display_primitive(value=value) == {
        'list': ['red'],
        'tuple': ('red',),
        'set': {'red'},
        'frozenset': frozenset({'red'}),
    }


@mark.unit_testing
def test_to_display_primitive_converts_value_attributes_and_unknown_objects() -> None:
    """
    Test display conversion handles value wrappers and unknown objects.
    """
    assert to_display_primitive(value=DisplayColorValueAttribute()) == 'red'
    assert to_display_primitive(value=object()).startswith('<object object at ')


@mark.unit_testing
def test_to_display_primitive_returns_string_when_to_primitives_is_available() -> None:
    """
    Test display conversion does not call an object's to_primitives method.
    """
    assert to_display_primitive(value=SelfToPrimitives()) == 'self-to-primitives'
