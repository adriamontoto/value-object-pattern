"""
Value object for typed dictionary values.
"""

from __future__ import annotations

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from collections.abc import Iterator
from inspect import isclass
from types import UnionType
from typing import (
    Any,
    ClassVar,
    Generic,
    ItemsView,
    KeysView,
    NoReturn,
    Self,
    TypeVar,
    Union,
    ValuesView,
    cast,
    get_args,
    get_origin,
)

from value_object_pattern.decorators import validation
from value_object_pattern.models import ValueObject
from value_object_pattern.models.primitive_conversion import from_primitive, to_primitive
from value_object_pattern.models.type_matching import matches_expected_type

K = TypeVar('K', bound=Any)
V = TypeVar('V', bound=Any)


def _validate_dict_type_argument(*, type_argument: Any) -> None:
    """
    Validate a type argument used by DictValueObject.

    Args:
        type_argument: The type argument to validate.

    Raises:
        TypeError: If the type argument is not a type-like annotation.
    """
    if isinstance(type_argument, TypeVar):
        return

    if type(type_argument) is not type and not isclass(object=type_argument) and get_origin(tp=type_argument) is None:
        raise TypeError(f'DictValueObject[...] <<<{type_argument}>>> must be a type. Got <<<{type(type_argument).__name__}>>> type.')  # noqa: E501  # fmt: skip


def _parse_dict_type_arguments(*, type_arguments: Any) -> tuple[Any, Any]:
    """
    Return key and value type arguments from `DictValueObject[K, V]` input.

    Args:
        type_arguments: The raw type arguments passed to `DictValueObject[...]`.

    Raises:
        TypeError: If exactly two type arguments are not provided.

    Returns:
        tuple[Any, Any]: The key and value type arguments.
    """
    if not isinstance(type_arguments, tuple):
        raise TypeError('DictValueObject must be parameterised, e.g. `class StrIntDict(DictValueObject[str, int])`.')

    if len(type_arguments) != 2:
        raise TypeError('DictValueObject must be parameterised, e.g. `class StrIntDict(DictValueObject[str, int])`.')

    key_type, value_type = type_arguments

    return key_type, value_type


class _DictValueObjectAlias:
    """
    Runtime alias returned by `DictValueObject[K, V]`.

    Key and value types must be available before `ValueObject.__init__` validates the dictionary. This alias keeps
    subclass declarations working through `__mro_entries__` and supports direct inline construction by creating a
    parameterized runtime subclass before validation starts.
    """

    _runtime_classes: ClassVar[dict[Any, type[DictValueObject[Any, Any]]]] = {}

    def __init__(self, *, origin: type[DictValueObject[Any, Any]], key_type: Any, value_type: Any) -> None:
        """
        Create a runtime alias for a parameterized DictValueObject.

        Args:
            origin: The original DictValueObject class.
            key_type: The key type argument used in `DictValueObject[K, V]`.
            value_type: The value type argument used in `DictValueObject[K, V]`.
        """
        self.__origin__ = origin
        self.__args__ = (key_type, value_type)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Construct an inline parameterized DictValueObject instance.

        Args:
            *args: Positional arguments passed to the generated value object subclass.
            **kwargs: Keyword arguments passed to the generated value object subclass.

        Returns:
            Any: The constructed value object.
        """
        return self._runtime_class()(*args, **kwargs)

    def __getattr__(self, name: str) -> Any:
        """
        Delegate class attribute access to the generated runtime subclass.

        Args:
            name: The attribute name to retrieve.

        Returns:
            Any: The resolved attribute.
        """
        return getattr(self._runtime_class(), name)

    def __mro_entries__(self, bases: tuple[type, ...]) -> tuple[type[DictValueObject[Any, Any]], ...]:
        """
        Return the origin class when the alias is used as a base class.

        Args:
            bases: The original class bases supplied by Python.

        Returns:
            tuple[type[DictValueObject[Any, Any]], ...]: The base classes to use for MRO construction.
        """
        _ = bases

        return (self.__origin__,)

    def _runtime_class(self) -> type[DictValueObject[Any, Any]]:
        """
        Return the generated runtime subclass for this alias.

        Returns:
            type[DictValueObject[Any, Any]]: The runtime subclass.
        """
        key_type, value_type = self.__args__
        _validate_dict_type_argument(type_argument=key_type)
        _validate_dict_type_argument(type_argument=value_type)
        key = (self.__origin__, key_type, value_type)
        if key not in self._runtime_classes:
            self._runtime_classes[key] = type(
                f'{self.__origin__.__name__}[{self._format_type_argument(type=key_type)}, {self._format_type_argument(type=value_type)}]',  # noqa: E501
                (self.__origin__,),
                {
                    '_is_inline_parameterized_dict_value_object': True,
                    '_key_type': key_type,
                    '_value_type': value_type,
                },
            )

        return self._runtime_classes[key]

    @staticmethod
    def _format_type_argument(*, type: Any) -> str:
        """
        Return a compact type-argument label for generated runtime class names.

        Args:
            type: The type argument to format.

        Returns:
            str: A readable type label.
        """
        origin = get_origin(tp=type)
        if origin in (Union, UnionType):
            return ' | '.join(_DictValueObjectAlias._format_type_argument(type=allowed) for allowed in get_args(type))

        if hasattr(type, '__name__'):
            return type.__name__  # type: ignore[no-any-return]

        return str(type).replace('typing.', '')


class DictValueObject(ValueObject[dict[K, V]], Generic[K, V]):  # noqa: UP046
    """
    Validate dictionary values, keys, and items against declared key and value types.

    `DictValueObject[K, V]` behaves like an immutable dictionary wrapper. Helpers such as `add()` and `delete()` return
    new value-object instances, while primitive helpers convert raw keys and values before applying the operation.

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

    @classmethod
    def __class_getitem__(cls, item: Any) -> Any:
        """
        Return a runtime alias that supports subclassing and inline construction.

        Args:
            item: The type arguments used in `DictValueObject[item]`.

        Returns:
            Any: A runtime alias for the parameterized DictValueObject.
        """
        key_type, value_type = _parse_dict_type_arguments(type_arguments=item)

        return _DictValueObjectAlias(origin=cls, key_type=key_type, value_type=value_type)

    @override
    def __init_subclass__(cls, **kwargs: Any) -> None:
        """
        Capture and validate key and value types declared by a subclass.

        Args:
            **kwargs: Keyword arguments forwarded to the parent class hook.

        Raises:
            TypeError: If the key type is not a type-like annotation.
            TypeError: If the value type is not a type-like annotation.
            TypeError: If the subclass is not parameterized with `DictValueObject[K, V]`.
        """
        super().__init_subclass__(**kwargs)

        if getattr(cls, '_is_inline_parameterized_dict_value_object', False):
            return

        for base in getattr(cls, '__orig_bases__', ()):
            if get_origin(base) is DictValueObject or getattr(base, '__origin__', None) is DictValueObject:
                key_type, val_type = get_args(base) or base.__args__

                _validate_dict_type_argument(type_argument=key_type)
                cls._key_type = key_type
                _validate_dict_type_argument(type_argument=val_type)
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

        for key in value.keys():  # noqa: SIM118
            if not matches_expected_type(value=key, expected_type=self._key_type):
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

        for item in value.values():
            if not matches_expected_type(value=item, expected_type=self._value_type):
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
        if default is not None and not matches_expected_type(value=default, expected_type=self._value_type):
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

    @classmethod
    def from_primitives(cls, value: dict[Any, Any]) -> Self:
        """
        Creates a DictValueObject from a dictionary of primitives.

        Args:
            value (dict[Any, Any]): The dictionary of primitives.

        Returns:
            Self: The created DictValueObject.

        Raises:
            TypeError: If the `value` is not a dict.

        Example:
        ```python
        from value_object_pattern.models import ValueObject
        from value_object_pattern.models.collections import DictValueObject


        class Age(ValueObject[int]):
            pass


        class StrAgeDict(DictValueObject[str, Age]):
            pass


        dictionary = StrAgeDict.from_primitives(value={'john': 30, 'jane': 25})
        print({key: age.value for key, age in dictionary.items()})
        # >>> {'john': 30, 'jane': 25}
        ```
        """
        if not isinstance(cast(Any, value), dict):
            return cls(value=value)

        dictionary: dict[Any, Any] = {}

        for key, item in value.items():
            primitive_key = from_primitive(value=key, expected_type=cls._key_type)
            primitive_value = from_primitive(value=item, expected_type=cls._value_type)
            dictionary[primitive_key] = primitive_value

        return cls(value=dictionary)

    def to_primitives(self) -> dict[Any, Any]:
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
        dictionary: dict[Any, Any] = {}
        for key, value in self._value.items():
            primitive_key = to_primitive(value=key)
            primitive_value = to_primitive(value=value)
            dictionary[primitive_key] = primitive_value

        return dictionary
