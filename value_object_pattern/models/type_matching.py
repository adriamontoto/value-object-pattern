"""
Helpers for runtime type matching used by generic value objects.
"""

from __future__ import annotations

from inspect import isclass
from types import UnionType
from typing import Any, Union, get_args, get_origin


def matches_expected_type(*, value: Any, expected_type: Any) -> bool:
    """
    Returns whether `value` matches `expected_type`, supporting typing unions and Any.

    This matcher keeps Python subclass semantics for most classes, with one important
    exception: `bool` does not match `int` unless `bool` is explicitly included in the
    expected type.

    Args:
        value (Any): The value to check.
        expected_type (Any): The expected type, which may be a typing union or Any.

    Returns:
        bool: Whether the value matches the expected type.
    """
    if expected_type is Any:
        return True

    origin = get_origin(tp=expected_type)
    if origin in (Union, UnionType):
        return any(matches_expected_type(value=value, expected_type=allowed) for allowed in get_args(expected_type))

    expected = origin or expected_type
    if expected is type(None):
        return value is None

    # In Python, bool is a subclass of int. Keep them distinct unless bool is explicit.
    if expected is int:
        return type(value) is int

    if expected is bool:
        return type(value) is bool

    if not isclass(object=expected):
        try:
            return isinstance(value, expected)
        except TypeError:
            return False

    return isinstance(value, expected)
