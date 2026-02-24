"""
Utilities for recursive primitive conversion.
"""

from __future__ import annotations

from enum import Enum
from inspect import _empty, isclass
from types import UnionType
from typing import Any, Union, get_args, get_origin

from .type_matching import matches_expected_type
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


def from_primitive(*, value: Any, expected_type: Any) -> Any:
    """
    Recursively converts a primitive value into the provided expected type.

    Args:
        value (Any): Primitive value to convert.
        expected_type (Any): Target type annotation or class.

    Returns:
        Any: Converted value.
    """
    if expected_type in (_empty, Any):
        return value

    origin = get_origin(tp=expected_type)
    if origin in (Union, UnionType):
        return _convert_union_from_primitive(value=value, expected_type=expected_type)

    if origin is not None:
        return _convert_collection_from_primitive(value=value, expected_type=expected_type)

    return _convert_single_from_primitive(value=value, expected_type=expected_type)


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


def _convert_union_from_primitive(*, value: Any, expected_type: Any) -> Any:
    """
    Converts a primitive using the first matching union candidate.

    Args:
        value (Any): Primitive value.
        expected_type (Any): Union annotation.

    Returns:
        Any: Converted value or the raw value if no candidate matches.
    """
    last_error: Exception | None = None
    for allowed_type in get_args(expected_type):
        try:
            converted_value = from_primitive(value=value, expected_type=allowed_type)

        except Exception as error:
            last_error = error
            continue

        if matches_expected_type(value=converted_value, expected_type=allowed_type):
            return converted_value

    _ = last_error
    return value


def _convert_collection_from_primitive(*, value: Any, expected_type: Any) -> Any:
    """
    Converts collection primitives recursively.

    Args:
        value (Any): Primitive value.
        expected_type (Any): Collection annotation.

    Returns:
        Any: Converted collection.
    """
    origin = get_origin(tp=expected_type)
    arguments = get_args(expected_type)
    handlers = {
        list: _convert_list_from_primitive,
        tuple: _convert_tuple_from_primitive,
        set: _convert_set_from_primitive,
        frozenset: _convert_frozenset_from_primitive,
        dict: _convert_dict_from_primitive,
    }

    handler = handlers.get(origin)
    if handler is None:
        return value

    return handler(value=value, arguments=arguments)


def _convert_list_from_primitive(*, value: Any, arguments: tuple[Any, ...]) -> Any:
    """
    Converts list primitives recursively.

    Args:
        value (Any): Primitive value.
        arguments (tuple[Any, ...]): List type arguments.

    Returns:
        Any: Converted list or raw value.
    """
    if not isinstance(value, list):
        return value

    item_type = arguments[0] if arguments else Any
    return [from_primitive(value=item, expected_type=item_type) for item in value]


def _convert_tuple_from_primitive(*, value: Any, arguments: tuple[Any, ...]) -> Any:
    """
    Converts tuple primitives recursively.

    Args:
        value (Any): Primitive value.
        arguments (tuple[Any, ...]): Tuple type arguments.

    Returns:
        Any: Converted tuple or raw value.
    """
    if not isinstance(value, (list, tuple)):
        return value

    sequence = tuple(value)
    if len(arguments) == 2 and arguments[1] is Ellipsis:
        item_type = arguments[0]
        return tuple(from_primitive(value=item, expected_type=item_type) for item in sequence)

    if len(arguments) != len(sequence):
        return sequence

    return tuple(
        from_primitive(value=item, expected_type=item_type)
        for item, item_type in zip(sequence, arguments, strict=False)
    )


def _convert_set_from_primitive(*, value: Any, arguments: tuple[Any, ...]) -> Any:
    """
    Converts set primitives recursively.

    Args:
        value (Any): Primitive value.
        arguments (tuple[Any, ...]): Set type arguments.

    Returns:
        Any: Converted set or raw value.
    """
    if not isinstance(value, (set, frozenset, list, tuple)):
        return value

    item_type = arguments[0] if arguments else Any
    return {from_primitive(value=item, expected_type=item_type) for item in value}


def _convert_frozenset_from_primitive(*, value: Any, arguments: tuple[Any, ...]) -> Any:
    """
    Converts frozenset primitives recursively.

    Args:
        value (Any): Primitive value.
        arguments (tuple[Any, ...]): Frozenset type arguments.

    Returns:
        Any: Converted frozenset or raw value.
    """
    if not isinstance(value, (set, frozenset, list, tuple)):
        return value

    item_type = arguments[0] if arguments else Any
    return frozenset(from_primitive(value=item, expected_type=item_type) for item in value)


def _convert_dict_from_primitive(*, value: Any, arguments: tuple[Any, ...]) -> Any:
    """
    Converts dict primitives recursively.

    Args:
        value (Any): Primitive value.
        arguments (tuple[Any, ...]): Dict type arguments.

    Returns:
        Any: Converted dict or raw value.
    """
    if not isinstance(value, dict):
        return value

    key_type = arguments[0] if len(arguments) >= 1 else Any
    value_type = arguments[1] if len(arguments) >= 2 else Any
    return {
        from_primitive(value=key, expected_type=key_type): from_primitive(value=item, expected_type=value_type)
        for key, item in value.items()
    }


def _convert_single_from_primitive(*, value: Any, expected_type: Any) -> Any:
    """
    Converts non-collection primitive values.

    Args:
        value (Any): Primitive value.
        expected_type (Any): Target class/type.

    Returns:
        Any: Converted value.
    """
    if expected_type is type(None):
        return None if value is None else value

    if not isclass(object=expected_type):
        return value

    converted = _convert_single_class_from_primitive(value=value, expected_type=expected_type)
    if converted is not _MISSING:
        return converted

    return value


def _convert_single_class_from_primitive(*, value: Any, expected_type: type[Any]) -> Any:
    """
    Converts class-based values from primitives.

    Args:
        value (Any): Primitive value.
        expected_type (type[Any]): Target class type.

    Returns:
        Any: Converted value or sentinel when no conversion applies.
    """
    if issubclass(expected_type, Enum):
        return _convert_enum_class_from_primitive(value=value, expected_type=expected_type)

    if issubclass(expected_type, ValueObject):
        return _convert_value_object_class_from_primitive(value=value, expected_type=expected_type)

    converted = _convert_from_primitives_class_from_primitive(value=value, expected_type=expected_type)
    if converted is not _MISSING:
        return converted

    if hasattr(expected_type, 'value'):
        if isinstance(value, expected_type):
            return value

        return expected_type(value=value)

    return _MISSING


def _convert_enum_class_from_primitive(*, value: Any, expected_type: type[Any]) -> Any:
    """
    Converts values to enum members.

    Args:
        value (Any): Primitive value.
        expected_type (type[Any]): Enum class.

    Returns:
        Any: Enum value.
    """
    if isinstance(value, expected_type):
        return value

    return expected_type(value)


def _convert_value_object_class_from_primitive(*, value: Any, expected_type: type[Any]) -> Any:
    """
    Converts values to ValueObject instances.

    Args:
        value (Any): Primitive value.
        expected_type (type[Any]): ValueObject class.

    Returns:
        Any: Converted ValueObject.
    """
    if isinstance(value, expected_type):
        return value

    from_primitives_method = getattr(expected_type, 'from_primitives', None)
    if callable(from_primitives_method):
        return from_primitives_method(value)

    return expected_type(value=value)


def _convert_from_primitives_class_from_primitive(*, value: Any, expected_type: type[Any]) -> Any:
    """
    Converts values using `from_primitives` for non-ValueObject classes.

    Args:
        value (Any): Primitive value.
        expected_type (type[Any]): Target class type.

    Returns:
        Any: Converted value or sentinel when conversion does not apply.
    """
    from_primitives_method = getattr(expected_type, 'from_primitives', None)
    if not callable(from_primitives_method):
        return _MISSING

    return _convert_with_from_primitives(
        value=value,
        expected_type=expected_type,
        from_primitives_method=from_primitives_method,
    )


def _convert_with_from_primitives(*, value: Any, expected_type: Any, from_primitives_method: Any) -> Any:
    """
    Converts values using a `from_primitives` classmethod when compatible.

    Args:
        value (Any): Primitive value.
        expected_type (Any): Target type.
        from_primitives_method (Any): Method to perform conversion.

    Returns:
        Any: Converted value or raw value when not compatible.
    """
    if isinstance(value, expected_type):
        return value

    if isinstance(value, dict):
        return from_primitives_method(value)

    to_primitives_method = getattr(value, 'to_primitives', None)
    if callable(to_primitives_method):
        primitives_value = to_primitives_method()
        try:
            return from_primitives_method(primitives_value)
        except Exception:
            return _MISSING

    return _MISSING
