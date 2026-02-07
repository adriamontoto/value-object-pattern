"""
DictValueObject module.
"""

from __future__ import annotations

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from collections.abc import Iterator
from enum import Enum
from inspect import isclass
from types import UnionType
from typing import Any, Generic, ItemsView, KeysView, NoReturn, TypeVar, Union, ValuesView, get_args, get_origin

from value_object_pattern.decorators import validation
from value_object_pattern.models import BaseModel, ValueObject

K = TypeVar('K', bound=Any)
V = TypeVar('V', bound=Any)


class DictValueObject(ValueObject[dict[K, V]], Generic[K, V]):  # noqa: UP046
    """
    DictValueObject is a value object that guarantees the wrapped value is a dictionary.

    Example:
    ```python
    from value_object_pattern.models.collections import DictValueObject


    class StrIntDict(DictValueObject[str, int]):
        pass


    dictionary = StrIntDict(value={'a': 1, 'b': 2})
    print(dictionary)
    print('a' in dictionary)
    print(list(dictionary))
    # >>> {'a': 1, 'b': 2}
    # >>> True
    # >>> ['a', 'b']
    ```
    """

    _key_type: K
    _value_type: V

    @override
    def __init_subclass__(cls, **kwargs: Any) -> None:
        """
        Initializes the class.

        Args:
            **kwargs (Any): Keyword arguments.

        Raises:
            TypeError: If the key is not a type.
            TypeError: If the value is not a type.
            TypeError: If the class is not parameterized.
        """
        super().__init_subclass__(**kwargs)

        for base in getattr(cls, '__orig_bases__', ()):
            if get_origin(base) is DictValueObject:
                key_type, val_type, *_ = get_args(base)

                if isinstance(key_type, TypeVar):
                    cls._key_type = key_type  # type: ignore[assignment]
                else:
                    if type(key_type) is not type and not isclass(key_type) and get_origin(key_type) is None:
                        raise TypeError(f'DictValueObject[...] <<<{key_type}>>> must be a type. Got <<<{type(key_type).__name__}>>> type.')  # noqa: E501  # fmt: skip

                    cls._key_type = key_type

                if isinstance(val_type, TypeVar):
                    cls._value_type = val_type  # type: ignore[assignment]
                else:
                    if type(val_type) is not type and not isclass(val_type) and get_origin(val_type) is None:
                        raise TypeError(f'DictValueObject[...] <<<{val_type}>>> must be a type. Got <<<{type(val_type).__name__}>>> type.')  # noqa: E501  # fmt: skip

                    cls._value_type = val_type

                return

        raise TypeError('DictValueObject must be parameterised, e.g. `class StrIntDict(DictValueObject[str, int])`.')

    def __contains__(self, key: Any) -> bool:
        """
        Returns True if the value object value contains the item, otherwise False.

        Args:
            item (Any): The item to check.

        Returns:
            bool: True if the value object value contains the item, otherwise False.

        Example:
        ```python
        from value_object_pattern.models.collections import DictValueObject


        class StrIntDict(DictValueObject[str, int]):
            pass


        dictionary = StrIntDict(value={'a': 1, 'b': 2})
        print('a' in dictionary)
        # >>> True
        ```
        """
        return key in self._value

    def __iter__(self) -> Iterator[K]:
        """
        Returns an iterator over the keys of the value object value.

        Returns:
            Iterator[K]: An iterator over the keys of the value object value.

        Example:
        ```python
        from value_object_pattern.models.collections import DictValueObject


        class StrIntDict(DictValueObject[str, int]):
            pass


        dictionary = StrIntDict(value={'a': 1, 'b': 2})
        print(list(dictionary))
        # >>> ['a', 'b']
        ```
        """
        return iter(self._value)

    def __reversed__(self) -> Iterator[K]:
        """
        Returns a reversed iterator over the keys of the value object value.

        Returns:
            Iterator[K]: A reversed iterator over the keys of the value object value.

        Example:
        ```python
        from value_object_pattern.models.collections import DictValueObject


        class StrIntDict(DictValueObject[str, int]):
            pass


        dictionary = StrIntDict(value={'a': 1, 'b': 2})
        print(list(dictionary))
        # >>> ['b', 'a']
        ```
        """
        return reversed(self._value)

    def __len__(self) -> int:
        """
        Returns the length of the value object value.

        Returns:
            int: The length of the value object value.

        Example:
        ```python
        from value_object_pattern.models.collections import DictValueObject


        class StrIntDict(DictValueObject[str, int]):
            pass


        dictionary = StrIntDict(value={'a': 1, 'b': 2})
        print(len(dictionary))
        # >>> 2
        ```
        """
        return len(self._value)

    def __getitem__(self, key: K) -> V:
        """
        Returns the value for the specified key.

        Args:
            key (K): The key to get the value for.

        Raises:
            KeyError: If the key is not found.

        Returns:
            V: The value for the specified key.

        Example:
        ```python
        from value_object_pattern.models.collections import DictValueObject


        class StrIntDict(DictValueObject[str, int]):
            pass


        dictionary = StrIntDict(value={'a': 1, 'b': 2})
        print(dictionary['a'])
        # >>> 1
        ```
        """
        return self._value[key]

    def items(self) -> ItemsView[K, V]:
        """
        Returns a view object that displays a list of dictionary's (key, value) tuple pairs.

        Returns:
            ItemsView[K, V]: A view object of the dictionary's items.

        Example:
        ```python
        from value_object_pattern.models.collections import DictValueObject


        class StrIntDict(DictValueObject[str, int]):
            pass


        dictionary = StrIntDict(value={'a': 1, 'b': 2})
        print(list(dictionary.items()))
        # >>> [('a', 1), ('b', 2)]
        ```
        """
        return self._value.items()

    def keys(self) -> KeysView[K]:
        """
        Returns a view object that displays a list of all the keys in the dictionary.

        Returns:
            KeysView[K]: A view object of the dictionary's keys.

        Example:
        ```python
        from value_object_pattern.models.collections import DictValueObject


        class StrIntDict(DictValueObject[str, int]):
            pass


        dictionary = StrIntDict(value={'a': 1, 'b': 2})
        print(list(dictionary.keys()))
        # >>> ['a', 'b']
        ```
        """
        return self._value.keys()

    def values(self) -> ValuesView[V]:
        """
        Returns a view object that displays a list of all the values in the dictionary.

        Returns:
            ValuesView[V]: A view object of the dictionary's values.

        Example:
        ```python
        from value_object_pattern.models.collections import DictValueObject


        class StrIntDict(DictValueObject[str, int]):
            pass


        dictionary = StrIntDict(value={'a': 1, 'b': 2})
        print(list(dictionary.values()))
        # >>> [1, 2]
        ```
        """
        return self._value.values()

    # def __repr__(self) -> str:
    # def __str__(self) -> str:

    @validation(order=0)
    def _ensure_value_is_from_dict(self, value: dict[Any, Any]) -> None:
        """
        Ensures the value object `value` is a dict.

        Args:
            value (dict[Any, Any]): The provided value.

        Raises:
            TypeError: If the `value` is not a dict.
        """
        if not isinstance(value, dict):
            self._raise_not_is_not_dict(value)

    def _raise_not_is_not_dict(self, value: Any) -> NoReturn:
        """
        Raises a TypeError if the value object `value` is not a dict.

        Args:
            value (Any): The provided value.

        Raises:
            TypeError: If the `value` is not a dict.
        """
        raise TypeError(f'DictValueObject value <<<{value}>>> must be a dict. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip

    @validation(order=1)
    def _ensure_keys_is_of_type(self, value: dict[K, V]) -> None:
        """
        Ensures the value object `value` is of type `K`.

        Args:
            value (dict[K, V]): The provided value.

        Raises:
            TypeError: If the `value` is not of type `K`.
        """
        if self._key_type is Any:
            return

        origin = get_origin(tp=self._key_type)
        if origin in (Union, UnionType):
            allowed_types: list[type[Any] | UnionType] = []
            for allowed in get_args(self._key_type):
                if allowed is Any:
                    return

                allowed_origin = get_origin(tp=allowed)
                allowed_types.append(allowed_origin or allowed)

            for key in value.keys():  # noqa: SIM118
                if not any(isinstance(key, allowed) for allowed in allowed_types):
                    self._raise_key_is_not_of_type(value=key)

            return

        expected_type = origin or self._key_type
        for key in value.keys():  # noqa: SIM118
            if not isinstance(key, expected_type):
                self._raise_key_is_not_of_type(value=key)

    def _raise_key_is_not_of_type(self, value: Any) -> NoReturn:
        """
        Raises a TypeError if the value object `value` is not of type `K`.

        Args:
            value (Any): The provided value.

        Raises:
            TypeError: If the `value` is not of type `K`.
        """
        raise TypeError(f'DictValueObject value <<<{value}>>> must be of type <<<{self._type_label(type=self._key_type)}>>> type. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip

    @validation(order=2)
    def _ensure_value_is_of_type(self, value: dict[K, V]) -> None:
        """
        Ensures the value object `value` is of type `V`.

        Args:
            value (dict[K, V]): The provided value.

        Raises:
            TypeError: If the `value` is not of type `V`.
        """
        if self._value_type is Any:
            return

        origin = get_origin(tp=self._value_type)
        if origin in (Union, UnionType):
            allowed_types: list[type[Any] | UnionType] = []
            for allowed in get_args(self._value_type):
                if allowed is Any:
                    return

                allowed_origin = get_origin(tp=allowed)
                allowed_types.append(allowed_origin or allowed)

            for item in value.values():
                if not any(isinstance(item, allowed) for allowed in allowed_types):
                    self._raise_value_is_not_of_type(value=item)

            return

        expected_type = origin or self._value_type
        for item in value.values():
            if not isinstance(item, expected_type):
                self._raise_value_is_not_of_type(value=item)

    def _raise_value_is_not_of_type(self, value: Any) -> NoReturn:
        """
        Raises a TypeError if the value object `value` is not of type `V`.

        Args:
            value (Any): The provided value.

        Raises:
            TypeError: If the `value` is not of type `V`.
        """
        raise TypeError(f'DictValueObject value <<<{value}>>> must be of type <<<{self._type_label(type=self._value_type)}>>> type. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip

    def get(self, *, key: K, default: V | None = None) -> V | None:
        """
        Returns the value for the specified key if key is in dictionary, else default.

        Args:
            key (K): The key to get the value for.
            default (V | None, optional): The default value to return if the key is not found. Defaults to None.

        Returns:
            V | None: The value for the specified key if key is in dictionary, else default.

        Example:
        ```python
        from value_object_pattern.models.collections import DictValueObject


        class StrIntDict(DictValueObject[str, int]):
            pass


        dictionary = StrIntDict(value={'a': 1, 'b': 2})
        print(dictionary.get(key='c', default=3))
        # >>> 3
        ```
        """
        if default is not None and not self._is_instance_of_type(value=default, expected_type=self._value_type):
            self._raise_value_is_not_of_type(value=default)

        return self._value.get(key, default)

    def is_empty(self) -> bool:
        """
        Returns True if the value object value is empty, otherwise False.

        Returns:
            bool: True if the value object value is empty, otherwise False.

        Example:
        ```python
        from value_object_pattern.models.collections import DictValueObject


        class StrIntDict(DictValueObject[str, int]):
            pass


        dictionary = StrIntDict(value={'a': 1, 'b': 2})
        print(dictionary.is_empty())
        # >>> False
        ```
        """
        return not self._value

    @staticmethod
    def _is_instance_of_type(*, value: Any, expected_type: Any) -> bool:
        """
        Checks if the value matches the expected type, supporting unions and Any.

        Args:
            value (Any): The value to check.
            expected_type (Any): The expected type or typing annotation.

        Returns:
            bool: True if the value matches the expected type, otherwise False.
        """
        if expected_type is Any:
            return True

        origin = get_origin(tp=expected_type)
        if origin in (Union, UnionType):
            for allowed in get_args(expected_type):
                if allowed is Any:
                    return True

                allowed_origin = get_origin(tp=allowed) or allowed
                if isinstance(value, allowed_origin):
                    return True

            return False

        expected = origin or expected_type
        return isinstance(value, expected)

    @staticmethod
    def _type_label(*, type: Any) -> str:
        """
        Returns a readable label for the configured type, including unions.

        Args:
            type (Any): The type to format.

        Returns:
            str: The type label.
        """
        origin = get_origin(tp=type)
        if origin in (Union, UnionType):
            parts = [DictValueObject._format_single_type(type=allowed) for allowed in get_args(type)]
            return ' | '.join(parts)

        return DictValueObject._format_single_type(type=type)

    @staticmethod
    def _format_single_type(*, type: Any) -> str:
        """
        Formats a single type for error messages.

        Args:
            type (Any): The type to format.

        Returns:
            str: The formatted type.
        """
        if type is Any:
            return 'Any'

        if hasattr(type, '__name__'):
            return type.__name__  # type: ignore[no-any-return]

        return str(type).replace('typing.', '')

    def to_primitives(self) -> dict[Any, Any]:  # noqa: C901
        """
        Returns the dictionary as a dictionary of primitives, recursively converting each key and value.

        Returns:
            dict[Any, Any]: Dictionary of primitives representation.

        Example:
        ```python
        from value_object_pattern.models import ValueObject
        from value_object_pattern.models.collections import DictValueObject


        class Age(ValueObject[int]):
            pass


        class StrAgeDict(DictValueObject[str, Age]):
            pass


        dictionary = StrAgeDict(value={'john': Age(value=30), 'jane': Age(value=25)})
        print(dictionary.to_primitives())
        # >>> {'john': 30, 'jane': 25}
        ```
        """
        primitive_types: tuple[type, ...] = (int, float, str, bool, bytes, bytearray, memoryview, type(None))
        collection_types: tuple[type, ...] = (list, dict, tuple, set, frozenset)

        primitives_dict: dict[Any, Any] = {}
        for key, value in self._value.items():
            primitive_key = key
            if isinstance(key, BaseModel) or hasattr(key, 'to_primitives'):
                primitive_key = key.to_primitives()  # type: ignore[assignment]

            elif isinstance(key, Enum):
                primitive_key = key.value

            elif isinstance(key, ValueObject) or hasattr(key, 'value'):
                key_value = key.value

                if isinstance(key_value, Enum):
                    key_value = key_value.value

                primitive_key = key_value

            elif isinstance(key, primitive_types):  # noqa: SIM114
                pass

            elif isinstance(key, collection_types):
                pass

            else:
                primitive_key = str(object=key)  # type: ignore[assignment]

            primitive_value = value
            if isinstance(value, BaseModel) or hasattr(value, 'to_primitives'):
                primitive_value = value.to_primitives()  # type: ignore[assignment]

            elif isinstance(value, Enum):
                primitive_value = value.value

            elif isinstance(value, ValueObject) or hasattr(value, 'value'):
                val_value = value.value

                if isinstance(val_value, Enum):
                    val_value = val_value.value

                primitive_value = val_value

            elif isinstance(value, primitive_types):  # noqa: SIM114
                pass

            elif isinstance(value, collection_types):
                pass

            else:
                primitive_value = str(object=value)  # type: ignore[assignment]

            primitives_dict[primitive_key] = primitive_value

        return primitives_dict
