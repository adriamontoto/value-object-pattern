"""
Value object generic type.
"""

from abc import ABC
from inspect import getmembers, ismethod
from sys import version_info
from typing import Generic, NoReturn, TypeVar

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

T = TypeVar('T')


class ValueObject(ABC, Generic[T]):
    """
    ValueObject generic type.

    Example:
    ```python
    from value_object_pattern import ValueObject


    class IntegerValueObject(ValueObject[int]):
        pass


    integer = IntegerValueObject(value=10)
    print(repr(integer))
    # >>> IntegerValueObject(value=10)
    ```
    """

    __slots__ = ('_value',)
    __match_args__ = ('_value',)

    _value: T

    def __init__(self, *, value: T) -> None:
        """
        ValueObject value object constructor.

        Args:
            value (T): Value.

        Example:
        ```python
        from value_object_pattern import ValueObject


        class IntegerValueObject(ValueObject[int]):
            pass


        integer = IntegerValueObject(value=10)
        print(repr(integer))
        # >>> IntegerValueObject(value=10)
        ```
        """
        self._validate(value=value)
        value = self._process(value=value)

        object.__setattr__(self, '_value', value)

    @override
    def __repr__(self) -> str:
        """
        Returns a detailed string representation of the value object.

        Returns:
            str: A string representation of the value object in the format 'ClassName(value=value)'.

        Example:
        ```python
        from value_object_pattern import ValueObject


        class IntegerValueObject(ValueObject[int]):
            pass


        integer = IntegerValueObject(value=10)
        print(repr(integer))
        # >>> IntegerValueObject(value=10)
        ```
        """
        return f'{self.__class__.__name__}(value={self._value!s})'

    @override
    def __str__(self) -> str:
        """
        Returns a simple string representation of the value object.

        Returns:
            str: The string representation of the value object value.

        Example:
        ```python
        from value_object_pattern import ValueObject


        class IntegerValueObject(ValueObject[int]):
            pass


        integer = IntegerValueObject(value=10)
        print(integer)
        # >>> 10
        ```
        """
        return str(object=self._value)

    @override
    def __hash__(self) -> int:
        """
        Returns the hash of the value object.

        Returns:
            int: Hash of the value object.

        Example:
        ```python
        from value_object_pattern import ValueObject


        class IntegerValueObject(ValueObject[int]):
            pass


        integer = IntegerValueObject(value=10)
        print(hash(integer))
        # >>> 10
        ```
        """
        return hash(self._value)

    @override
    def __eq__(self, other: object) -> bool:
        """
        Check if the value object is equal to another value object.

        Args:
            other (object): Object to compare.

        Returns:
            bool: True if both objects are equal, otherwise False.

        Example:
        ```python
        from value_object_pattern import ValueObject


        class IntegerValueObject(ValueObject[int]):
            pass


        integer_a = IntegerValueObject(value=10)
        integer_b = IntegerValueObject(value=16)
        print(integer_a == integer_b)
        # >>> False
        ```
        """
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self._value == other.value

    @override
    def __setattr__(self, key: str, value: T) -> NoReturn:
        """
        Prevents modification or addition of attributes in the value object.

        Args:
            key (str): The name of the attribute.
            value (T): The value to be assigned to the attribute.

        Raises:
            AttributeError: If there is an attempt to modify an existing attribute.
            AttributeError: If there is an attempt to add a new attribute.
        """
        public_key = key.replace('_', '')
        public_slots1 = [slot.replace('_', '') for slot in self.__slots__]

        if key in self.__slots__:
            raise AttributeError(f'Cannot modify attribute "{key}" of immutable instance.')

        if public_key in public_slots1:
            raise AttributeError(f'Cannot modify attribute "{public_key}" of immutable instance.')

        raise AttributeError(f'{self.__class__.__name__} object has no attribute "{key}".')

    def _process(self, value: T) -> T:
        """
        This method processes the value object value after validation.

        Args:
            value (T): The value object value.

        Returns:
            T: The processed value object value.
        """
        methods = []
        for _, method in getmembers(object=self, predicate=ismethod):
            if getattr(method, '_is_process', False):
                methods.append(method)

        methods = sorted(methods, key=lambda method: getattr(method, '_order', method.__name__))
        for method in methods:
            value = method(value=value)

        return value

    def _validate(self, value: T) -> None:
        """
        This method validates that the value follows the domain rules, by executing all methods with the `@validation`
        decorator.

        Args:
            value (T): The value object value.
        """
        for _, method in getmembers(object=self, predicate=ismethod):
            if getattr(method, '_is_validation', False):
                method(value=value)

    @property
    def value(self) -> T:
        """
        Returns the value object value.

        Returns:
            T: The value object value.

        Example:
        ```python
        from value_object_pattern import ValueObject


        class IntegerValueObject(ValueObject[int]):
            pass


        integer = IntegerValueObject(value=10)
        print(integer.value)
        # >>> 10
        ```
        """
        return self._value
