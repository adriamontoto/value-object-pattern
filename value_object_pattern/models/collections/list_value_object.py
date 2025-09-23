"""
ListValueObject module.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from collections.abc import Iterator
from enum import Enum
from inspect import isclass
from typing import Any, Generic, NoReturn, Self, TypeVar, get_args, get_origin

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

        expected_type = get_origin(tp=self._type) or self._type
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
        raise TypeError(f'ListValueObject value <<<{value}>>> must be of type <<<{self._type.__name__}>>> type. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip

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

        for primitive in value:
            if hasattr(cls._type, 'from_primitives'):
                items.append(cls._type.from_primitives(primitive))  # BaseModel

            elif hasattr(cls._type, 'value'):
                items.append(cls._type(value=primitive))  # ValueObject

            else:
                items.append(primitive)

        return cls(value=items)
