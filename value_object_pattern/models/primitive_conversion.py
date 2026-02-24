"""
Utilities for recursive primitive conversion.
"""

from enum import Enum
from typing import Any

from .value_object import ValueObject

PRIMITIVE_TYPES: tuple[type, ...] = (int, float, str, bool, bytes, bytearray, memoryview, type(None))
_MISSING = object()


def to_primitive(value: Any) -> Any:
    """
    Recursively converts value objects, models, enums, and collections to primitives.

    Args:
        value (Any): Value to convert.

    Returns:
        Any: Primitive representation.
    """
    if isinstance(value, PRIMITIVE_TYPES):
        return value

    if isinstance(value, Enum):
        return to_primitive(value=value.value)

    primitive_value = _convert_with_to_primitives(value=value)
    if primitive_value is not _MISSING:
        return primitive_value

    primitive_value = _convert_with_value_attribute(value=value)
    if primitive_value is not _MISSING:
        return primitive_value

    if isinstance(value, (list, tuple, set, frozenset, dict)):
        return _convert_collection(value=value)

    return str(object=value)


def _convert_with_to_primitives(*, value: Any) -> Any:
    """
    Converts values exposing `to_primitives`, if available.

    Args:
        value (Any): Value to convert.

    Returns:
        Any: Converted value or sentinel when the branch does not apply.
    """
    to_primitives_method = getattr(value, 'to_primitives', None)
    if not callable(to_primitives_method):
        return _MISSING

    primitive_value = to_primitives_method()
    if primitive_value is value:
        return str(object=value)

    return to_primitive(value=primitive_value)


def _convert_with_value_attribute(*, value: Any) -> Any:
    """
    Converts value-like wrappers exposing a `value` attribute.

    Args:
        value (Any): Value to convert.

    Returns:
        Any: Converted value or sentinel when the branch does not apply.
    """
    if not (isinstance(value, ValueObject) or hasattr(value, 'value')):
        return _MISSING

    nested_value = getattr(value, 'value', value)
    if nested_value is value:
        return str(object=value)

    return to_primitive(value=nested_value)


def _convert_collection(*, value: Any) -> Any:
    """
    Recursively converts collection values to primitive collections.

    Args:
        value (Any): Collection value.

    Returns:
        Any: Converted collection.
    """
    if isinstance(value, list):
        return [to_primitive(value=item) for item in value]

    if isinstance(value, tuple):
        return tuple(to_primitive(value=item) for item in value)

    if isinstance(value, set):
        return {to_primitive(value=item) for item in value}

    if isinstance(value, frozenset):
        return frozenset(to_primitive(value=item) for item in value)

    return {to_primitive(value=key): to_primitive(value=item) for key, item in value.items()}
