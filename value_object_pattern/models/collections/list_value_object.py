"""
ListValueObject module.
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
from typing import Any, Generic, NoReturn, Self, TypeVar, Union, get_args, get_origin

from value_object_pattern.decorators import validation
from value_object_pattern.models import BaseModel, ValueObject

T = TypeVar('T', bound=Any)


class ListValueObject(ValueObject[list[T]], Generic[T]):  # noqa: UP046
    """
    ListValueObject is a value object that ensures the provided value is from a list.

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

    @override
    def __init_subclass__(cls, **kwargs: Any) -> None:
        """
        Initializes the class.

        Args:
            **kwargs (Any): Keyword arguments.

        Raises:
            TypeError: If the class parameter is not a type.
            TypeError: If the class is not parameterized.
        """
        super().__init_subclass__(**kwargs)

        for base in getattr(cls, '__orig_bases__', ()):
            if get_origin(tp=base) is ListValueObject:
                _type, *_ = get_args(tp=base)

                if isinstance(_type, TypeVar):
                    cls._type = _type  # type: ignore[assignment]
                    return

                if type(_type) is not type and not isclass(object=_type) and get_origin(tp=_type) is None:
                    raise TypeError(f'ListValueObject[...] <<<{_type}>>> must be a type. Got <<<{type(_type).__name__}>>> type.')  # noqa: E501  # fmt: skip

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

            elif isinstance(item, ValueObject) or hasattr(item, 'value'):
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

            elif isinstance(item, ValueObject) or hasattr(item, 'value'):
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

        origin = get_origin(tp=self._type)
        if origin in (Union, UnionType):
            allowed_types: list[type[Any] | UnionType] = []
            for allowed in get_args(self._type):
                if allowed is Any:
                    return

                allowed_origin = get_origin(tp=allowed)
                allowed_types.append(allowed_origin or allowed)

            for item in value:
                if not any(isinstance(item, allowed) for allowed in allowed_types):
                    self._raise_value_is_not_of_type(value=item)

            return

        expected_type = origin or self._type
        for item in value:
            if not isinstance(item, expected_type):
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
        item = self._convert_from_primitives(value=item)

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
        items = [self._convert_from_primitives(value=item) for item in items]

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
        item = self._convert_from_primitives(value=item)

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
        items = [self._convert_from_primitives(value=item) for item in items]

        return self.delete_all(items=items)

    def _convert_from_primitives(self, *, value: Any) -> T:
        """
        Converts a primitive value to the appropriate type T.

        Args:
            value (Any): The primitive value to convert.

        Returns:
            T: The converted value.
        """
        if hasattr(self._type, 'from_primitives'):
            return self._type.from_primitives(value)  # type: ignore[no-any-return]

        if get_origin(tp=self._type) in (Union, UnionType):
            return value  # type: ignore[no-any-return]

        if hasattr(self._type, 'value'):
            return self._type(value=value)  # type: ignore[no-any-return]

        return value  # type: ignore[no-any-return]

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
        """
        items: list[Any] = []

        for item in value:
            if hasattr(cls._type, 'from_primitives'):
                items.append(cls._type.from_primitives(item))  # BaseModel

            elif hasattr(cls._type, 'value'):
                items.append(cls._type(value=item))  # ValueObject

            else:
                items.append(item)

        return cls(value=items)

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
        primitive_types: tuple[type, ...] = (int, float, str, bool, bytes, bytearray, memoryview, type(None))
        collection_types: tuple[type, ...] = (list, dict, tuple, set, frozenset)

        primitives_list: list[Any] = []
        for item in self._value:
            if isinstance(item, BaseModel) or hasattr(item, 'to_primitives'):
                primitives_list.append(item.to_primitives())

            elif isinstance(item, Enum):
                primitives_list.append(item.value)

            elif isinstance(item, ValueObject) or hasattr(item, 'value'):
                value = item.value

                if isinstance(value, Enum):
                    value = value.value

                primitives_list.append(value)

            elif isinstance(item, primitive_types):  # noqa: SIM114
                primitives_list.append(item)

            elif isinstance(item, collection_types):
                primitives_list.append(item)

            else:
                primitives_list.append(str(object=item))

        return primitives_list
