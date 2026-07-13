"""
Value object for typed list values.
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
from typing import Any, ClassVar, Generic, NoReturn, Self, TypeVar, Union, cast, get_args, get_origin

from value_object_pattern.decorators import validation
from value_object_pattern.models import BaseModel, ValueObject
from value_object_pattern.models.primitive_conversion import from_primitive, to_primitive
from value_object_pattern.models.type_matching import matches_expected_type

T = TypeVar('T', bound=Any)


def _validate_list_type_argument(*, type_argument: Any) -> None:
    """
    Validate a type argument used by ListValueObject.

    Args:
        type_argument: The type argument to validate.

    Raises:
        TypeError: If the type argument is not a type-like annotation.
    """
    if isinstance(type_argument, TypeVar):
        return

    if type(type_argument) is not type and not isclass(object=type_argument) and get_origin(tp=type_argument) is None:
        raise TypeError(f'ListValueObject[...] <<<{type_argument}>>> must be a type. Got <<<{type(type_argument).__name__}>>> type.')  # noqa: E501  # fmt: skip


class _ListValueObjectAlias:
    """
    Runtime alias returned by `ListValueObject[T]`.

    The item type must be available before `ValueObject.__init__` validates the list. This alias keeps subclass
    declarations working through `__mro_entries__` and supports direct inline construction by creating a parameterized
    runtime subclass before validation starts.
    """

    _runtime_classes: ClassVar[dict[Any, type[ListValueObject[Any]]]] = {}

    def __init__(self, *, origin: type[ListValueObject[Any]], type_argument: Any) -> None:
        """
        Create a runtime alias for a parameterized ListValueObject.

        Args:
            origin: The original ListValueObject class.
            type_argument: The type argument used in `ListValueObject[T]`.
        """
        self.__origin__ = origin
        self.__args__ = (type_argument,)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Construct an inline parameterized ListValueObject instance.

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

    def __mro_entries__(self, bases: tuple[type, ...]) -> tuple[type[ListValueObject[Any]], ...]:
        """
        Return the origin class when the alias is used as a base class.

        Args:
            bases: The original class bases supplied by Python.

        Returns:
            tuple[type[ListValueObject[Any]], ...]: The base classes to use for MRO construction.
        """
        _ = bases

        return (self.__origin__,)

    def _runtime_class(self) -> type[ListValueObject[Any]]:
        """
        Return the generated runtime subclass for this alias.

        Returns:
            type[ListValueObject[Any]]: The runtime subclass.
        """
        type_argument, *_ = self.__args__
        _validate_list_type_argument(type_argument=type_argument)
        key = (self.__origin__, type_argument)
        if key not in self._runtime_classes:
            self._runtime_classes[key] = type(
                f'{self.__origin__.__name__}[{self._format_type_argument(type=type_argument)}]',
                (self.__origin__,),
                {
                    '_is_inline_parameterized_list_value_object': True,
                    '_type': type_argument,
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
            return ' | '.join(_ListValueObjectAlias._format_type_argument(type=allowed) for allowed in get_args(type))

        if hasattr(type, '__name__'):
            return type.__name__  # type: ignore[no-any-return]

        return str(type).replace('typing.', '')


class ListValueObject(ValueObject[list[T]], Generic[T]):  # noqa: UP046
    """
    Validate list values and every item against the declared item type.

    `ListValueObject[T]` stores an immutable wrapper around a list. Mutating helpers such as `add()`, `extend()`, and
    `delete()` return new value-object instances instead of changing the current object. Primitive helpers convert raw
    items into the declared item type before applying the operation.

    Example:
    ```python
    from value_object_pattern.models.collections import ListValueObject


    class IntListValueObject(ListValueObject[int]):
        pass


    sequence = IntListValueObject(value=[1, 2, 3])
    print(sequence)
    # >>> [1, 2, 3]
    ```
    """

    _type: T

    @classmethod
    def __class_getitem__(cls, item: Any) -> Any:
        """
        Return a runtime alias that supports subclassing and inline construction.

        Args:
            item: The type argument used in `ListValueObject[item]`.

        Returns:
            Any: A runtime alias for the parameterized ListValueObject.
        """
        return _ListValueObjectAlias(origin=cls, type_argument=item)

    @override
    def __init_subclass__(cls, **kwargs: Any) -> None:
        """
        Capture and validate the item type declared by a subclass.

        Args:
            **kwargs: Keyword arguments forwarded to the parent class hook.

        Raises:
            TypeError: If the class parameter is not a type-like annotation.
            TypeError: If the subclass is not parameterized with `ListValueObject[T]`.
        """
        super().__init_subclass__(**kwargs)

        if getattr(cls, '_is_inline_parameterized_list_value_object', False):
            return

        for base in getattr(cls, '__orig_bases__', ()):
            if get_origin(tp=base) is ListValueObject or getattr(base, '__origin__', None) is ListValueObject:
                _type, *_ = get_args(tp=base) or base.__args__

                _validate_list_type_argument(type_argument=_type)
                cls._type = _type
                return

        raise TypeError('ListValueObject must be parameterized, e.g. "class InIntListValueObject(ListValueObject[int])".')  # noqa: E501  # fmt: skip

    def __contains__(self, item: Any) -> bool:
        """
        Returns True if the value object value contains the item, otherwise False.

        Args:
            item (Any): The item to check.

        Returns:
            bool: True if the value object value contains the item, otherwise False.

        Example:
        ```python
        from value_object_pattern.models.collections import ListValueObject


        class IntListValueObject(ListValueObject[int]):
            pass


        sequence = IntListValueObject(value=[1, 2, 3])
        print(1 in sequence)
        # >>> True
        ```
        """
        return item in self._value

    def __iter__(self) -> Iterator[T]:
        """
        Returns an iterator over the value object value.

        Returns:
            Iterator[T]: An iterator over the value object value.

        Example:
        ```python
        from value_object_pattern.models.collections import ListValueObject


        class IntListValueObject(ListValueObject[int]):
            pass


        sequence = IntListValueObject(value=[1, 2, 3])
        print(list(sequence))
        # >>> [1, 2, 3]
        ```
        """
        return iter(self._value)

    def __len__(self) -> int:
        """
        Returns the length of the value object value.

        Returns:
            int: The length of the value object value.

        Example:
        ```python
        from value_object_pattern.models.collections import ListValueObject


        class IntListValueObject(ListValueObject[int]):
            pass


        sequence = IntListValueObject(value=[1, 2, 3])
        print(len(sequence))
        # >>> 3
        ```
        """
        return len(self._value)

    def __reversed__(self) -> Iterator[T]:
        """
        Returns a reversed iterator over the value object value.

        Returns:
            Iterator[T]: A reversed iterator over the value object value.

        Example:
        ```python
        from value_object_pattern.models.collections import ListValueObject


        class IntListValueObject(ListValueObject[int]):
            pass


        sequence = IntListValueObject(value=[1, 2, 3])
        print(list(reversed(sequence)))
        # >>> [3, 2, 1]
        ```
        """
        return reversed(self._value)

    @override
    def __repr__(self) -> str:
        """
        Returns the string representation of the value object value.

        Returns:
            str: The string representation of the value object value.

        Example:
        ```python
        from value_object_pattern.models.collections import ListValueObject


        class IntListValueObject(ListValueObject[int]):
            pass


        sequence = IntListValueObject(value=[1, 2, 3])
        print(repr(sequence))
        # >>> [1, 2, 3]
        ```
        """
        primitive_types: tuple[type, ...] = (int, float, str, bool, bytes, bytearray, memoryview, type(None))
        collection_types: tuple[type, ...] = (list, dict, tuple, set, frozenset)

        list_to_return: list[Any] = []
        for item in self._value:
            if isinstance(item, BaseModel):
                list_to_return.append(repr(item))

            elif isinstance(item, Enum):
                list_to_return.append(item.value)

            elif isinstance(item, ValueObject):
                value = item._value_for_display()

                if isinstance(value, Enum):
                    value = value.value

                list_to_return.append(repr(value))

            elif hasattr(item, 'value'):
                value = item.value

                if isinstance(value, Enum):
                    value = value.value

                list_to_return.append(repr(value))

            elif isinstance(item, primitive_types):  # noqa: SIM114
                list_to_return.append(item)

            elif isinstance(item, collection_types):
                list_to_return.append(repr(item))

            else:
                list_to_return.append(repr(item))

        return repr(list_to_return)

    @override
    def __str__(self) -> str:
        """
        Returns the string representation of the value object value.

        Returns:
            str: The string representation of the value object value.

        Example:
        ```python
        from value_object_pattern.models.collections import ListValueObject


        class IntListValueObject(ListValueObject[int]):
            pass


        sequence = IntListValueObject(value=[1, 2, 3])
        print(str(sequence))
        # >>> [1, 2, 3]
        ```
        """
        primitive_types: tuple[type, ...] = (int, float, str, bool, bytes, bytearray, memoryview, type(None))
        collection_types: tuple[type, ...] = (list, dict, tuple, set, frozenset)

        list_to_return: list[Any] = []
        for item in self._value:
            if isinstance(item, BaseModel):
                list_to_return.append(str(object=item))

            elif isinstance(item, Enum):
                list_to_return.append(item.value)

            elif isinstance(item, ValueObject):
                value = item._value_for_display()

                if isinstance(value, Enum):
                    value = value.value

                list_to_return.append(str(object=value))

            elif hasattr(item, 'value'):
                value = item.value

                if isinstance(value, Enum):
                    value = value.value

                list_to_return.append(str(object=value))

            elif isinstance(item, primitive_types):  # noqa: SIM114
                list_to_return.append(item)

            elif isinstance(item, collection_types):
                list_to_return.append(str(object=item))

            else:
                list_to_return.append(str(object=item))

        return str(object=list_to_return)

    @validation(order=0)
    def _ensure_value_is_from_list(self, value: list[Any]) -> None:
        """
        Ensures the value object `value` is a list.

        Args:
            value (list[Any]): The provided value.

        Raises:
            TypeError: If the `value` is not a list.
        """
        if not isinstance(value, list):
            self._raise_value_is_not_list(value=value)

    def _raise_value_is_not_list(self, value: Any) -> NoReturn:
        """
        Raises a TypeError if the value object `value` is not a list.

        Args:
            value (Any): The provided value.

        Raises:
            TypeError: If the `value` is not a list.
        """
        raise TypeError(f'ListValueObject value <<<{value}>>> must be a list. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip

    @validation(order=1)
    def _ensure_value_is_of_type(self, value: list[T]) -> None:
        """
        Ensures the value object `value` is of type `T`.

        Args:
            value (list[T]): The provided value.

        Raises:
            TypeError: If the `value` is not of type `T`.
        """
        if self._type is Any:
            return

        for item in value:
            if not matches_expected_type(value=item, expected_type=self._type):
                self._raise_value_is_not_of_type(value=item)

    def _raise_value_is_not_of_type(self, value: Any) -> NoReturn:
        """
        Raises a TypeError if the value object `value` is not of type `T`.

        Args:
            value (Any): The provided value.

        Raises:
            TypeError: If the `value` is not of type `T`.
        """
        raise TypeError(f'ListValueObject value <<<{value}>>> must be of type <<<{self._type_label()}>>> type. Got <<<{type(value).__name__}>>> type.')  # fmt: skip  # noqa: E501

    def is_empty(self) -> bool:
        """
        Returns True if the value object value is empty, otherwise False.

        Returns:
            bool: True if the value object value is empty, otherwise False.

        Example:
        ```python
        from value_object_pattern.models.collections import ListValueObject


        class IntListValueObject(ListValueObject[int]):
            pass


        sequence = IntListValueObject(value=[1, 2, 3])
        print(sequence.is_empty())
        # >>> False
        ```
        """
        return not self._value

    def add(self, *, item: T) -> Self:
        """
        Returns a new ListValueObject with the item added to the end.

        Args:
            item (T): The item to add.

        Raises:
            TypeError: If the item is not of type T.

        Returns:
            Self: A new ListValueObject with the item added.

        Example:
        ```python
        from value_object_pattern.models.collections import ListValueObject


        class IntListValueObject(ListValueObject[int]):
            pass


        sequence = IntListValueObject(value=[1, 2, 3])
        new_sequence = sequence.add(item=4)
        print(new_sequence)
        print(id(sequence) == id(new_sequence))
        # >>> [1, 2, 3, 4]
        # >>> False
        ```
        """
        return self.__class__(value=[*self._value, item])

    def add_from_primitives(self, *, item: Any) -> Self:
        """
        Returns a new ListValueObject with the item created from a primitives added to the end.

        Args:
            item (Any): The primitives item to convert and add.

        Raises:
            TypeError: If the item is not of type T.

        Returns:
            Self: A new ListValueObject with the item added.

        Example:
        ```python
        from value_object_pattern.models import ValueObject
        from value_object_pattern.models.collections import ListValueObject


        class Age(ValueObject[int]):
            pass


        class AgeListValueObject(ListValueObject[Age]):
            pass


        sequence = AgeListValueObject(value=[Age(value=10), Age(value=20)])
        new_sequence = sequence.add_from_primitives(item=30)
        print(new_sequence)
        print(id(sequence) == id(new_sequence))
        # >>> [10, 20, 30]
        # >>> False
        ```
        """
        item = from_primitive(value=item, expected_type=self._type)

        return self.add(item=item)

    def extend(self, *, items: list[T]) -> Self:
        """
        Returns a new ListValueObject with multiple items added to the end.

        Args:
            items (list[T]): The items to add.

        Raises:
            TypeError: If the items are not of the correct type.

        Returns:
            Self: A new ListValueObject with the items added.

        Example:
        ```python
        from value_object_pattern.models.collections import ListValueObject


        class IntListValueObject(ListValueObject[int]):
            pass


        sequence = IntListValueObject(value=[1, 2, 3])
        new_sequence = sequence.extend(items=[4, 5, 6])
        print(new_sequence)
        print(id(sequence) == id(new_sequence))
        # >>> [1, 2, 3, 4, 5, 6]
        # >>> False
        ```
        """
        return self.__class__(value=self._value + items)

    def extend_from_primitives(self, *, items: list[Any]) -> Self:
        """
        Returns a new ListValueObject with multiple items created from primitives added to the end.

        Args:
            items (list[Any]): The primitive items to convert and add.

        Raises:
            TypeError: If the items are not of the correct type.

        Returns:
            Self: A new ListValueObject with the items added.

        Example:
        ```python
        from value_object_pattern.models import ValueObject
        from value_object_pattern.models.collections import ListValueObject


        class Age(ValueObject[int]):
            pass


        class AgeListValueObject(ListValueObject[Age]):
            pass


        sequence = AgeListValueObject(value=[Age(value=10)])
        new_sequence = sequence.extend_from_primitives(items=[20, 30])
        print(new_sequence)
        print(id(sequence) == id(new_sequence))
        # >>> [10, 20, 30]
        # >>> False
        ```
        """
        items = [from_primitive(value=item, expected_type=self._type) for item in items]

        return self.extend(items=items)

    def delete(self, *, item: T) -> Self:
        """
        Returns a new ListValueObject with the first occurrence of the item deleted.

        Args:
            item (T): The item to delete.

        Raises:
            ValueError: If the item is not in the list.

        Returns:
            Self: A new ListValueObject with the item deleted.

        Example:
        ```python
        from value_object_pattern.models.collections import ListValueObject


        class IntListValueObject(ListValueObject[int]):
            pass


        sequence = IntListValueObject(value=[1, 2, 3, 2])
        new_sequence = sequence.delete(item=2)
        print(new_sequence)
        print(id(sequence) == id(new_sequence))
        # >>> [1, 3, 2]
        # >>> False
        ```
        """
        items = self._value.copy()

        try:
            items.remove(item)

        except ValueError:
            self._raise_value_not_found_when_deleting(value=item)

        return self.__class__(value=items)

    def _raise_value_not_found_when_deleting(self, value: Any) -> NoReturn:
        """
        Raises a ValueError if the item to be deleted is not found.

        Args:
            value (Any): The item to be deleted.

        Raises:
            ValueError: If the item is not found.
        """
        raise ValueError(f'ListValueObject item <<<{value}>>> not found in thelist when attempting to delete it.')

    def delete_from_primitives(self, *, item: Any) -> Self:
        """
        Returns a new ListValueObject with the first occurrence of an item matching the primitive deleted.

        Args:
            item (Any): The primitive value to convert and delete.

        Raises:
            ValueError: If the item is not in the list.

        Returns:
            Self: A new ListValueObject with the item deleted.

        Example:
        ```python
        from value_object_pattern.models import ValueObject
        from value_object_pattern.models.collections import ListValueObject


        class Age(ValueObject[int]):
            pass


        class AgeListValueObject(ListValueObject[Age]):
            pass


        sequence = AgeListValueObject(value=[Age(value=10), Age(value=20)])
        new_sequence = sequence.delete_from_primitives(item=10)
        print(new_sequence)
        print(id(sequence) == id(new_sequence))
        # >>> [20]
        # >>> False
        ```
        """
        item = from_primitive(value=item, expected_type=self._type)

        return self.delete(item=item)

    def delete_all(self, *, items: list[T]) -> Self:
        """
        Returns a new ListValueObject with all occurrences of the specified items deleted.

        Args:
            items (list[T]): The items to delete.

        Raises:
            ValueError: If any item is not in the list.

        Returns:
            Self: A new ListValueObject with the items deleted.

        Example:
        ```python
        from value_object_pattern.models.collections import ListValueObject


        class IntListValueObject(ListValueObject[int]):
            pass


        sequence = IntListValueObject(value=[1, 2, 3, 2, 4])
        new_sequence = sequence.delete_all(items=[2, 4])
        print(new_sequence)
        print(id(sequence) == id(new_sequence))
        # >>> [1, 3]
        # >>> False
        ```
        """
        new_list = [item for item in self._value if item not in items]

        for item in items:
            if item not in self._value:
                self._raise_value_not_found_when_deleting(value=item)

        return self.__class__(value=new_list)

    def delete_all_from_primitives(self, *, items: list[Any]) -> Self:
        """
        Returns a new ListValueObject with all occurrences of items matching the primitives deleted.

        Args:
            items (list[Any]): The primitive values to convert and delete.

        Raises:
            ValueError: If any item is not in the list.

        Returns:
            Self: A new ListValueObject with the items deleted.

        Example:
        ```python
        from value_object_pattern.models.collections import ListValueObject
        from value_object_pattern.models import ValueObject


        class Age(ValueObject[int]):
            pass


        class AgeListValueObject(ListValueObject[Age]):
            pass


        sequence = AgeListValueObject(value=[Age(value=10), Age(value=20), Age(value=30)])
        new_sequence = sequence.delete_all_from_primitives(items=[10, 30])
        print(new_sequence)
        print(id(sequence) == id(new_sequence))
        # >>> [20]
        # >>> False
        ```
        """
        items = [from_primitive(value=item, expected_type=self._type) for item in items]

        return self.delete_all(items=items)

    def _type_label(self) -> str:
        """
        Returns a readable label for the configured type, including unions.

        Returns:
            str: The type label.
        """
        origin = get_origin(tp=self._type)
        if origin in (Union, UnionType):
            parts = [self._format_single_type(type=type) for type in get_args(self._type)]
            return ' | '.join(parts)

        return self._format_single_type(type=self._type)

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
    def from_primitives(cls, value: list[Any]) -> Self:
        """
        Creates a ListValueObject from a list of primitives.

        Args:
            value (list[Any]): The list of primitives.

        Returns:
            Self: The created ListValueObject.

        Example:
        ```python
        from value_object_pattern.models import ValueObject
        from value_object_pattern.models.collections import ListValueObject


        class Age(ValueObject[int]):
            pass


        class AgeListValueObject(ListValueObject[Age]):
            pass


        age_list = AgeListValueObject.from_primitives(value=[10, 20, 30])
        print([age.value for age in age_list])
        # >>> [10, 20, 30]
        ```
        """
        if not isinstance(cast(Any, value), list):
            return cls(value=value)

        return cls(value=[from_primitive(value=item, expected_type=cls._type) for item in value])

    def to_primitives(self) -> list[Any]:
        """
        Returns the list as a list of primitives, recursively converting each item.

        Returns:
            list[Any]: List of primitives representation.

        Example:
        ```python
        from value_object_pattern.models import ValueObject
        from value_object_pattern.models.collections import ListValueObject


        class Age(ValueObject[int]):
            pass


        class AgeListValueObject(ListValueObject[Age]):
            pass


        sequence = AgeListValueObject(value=[Age(value=10), Age(value=20)])
        print(sequence.to_primitives())
        # >>> [10, 20]
        ```
        """
        return [to_primitive(value=item) for item in self._value]
