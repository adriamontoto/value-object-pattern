"""
Value object generic type.
"""

from abc import ABC
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
    """

    __slots__ = ('_value',)
    __match_args__ = ('_value',)

    _value: T

    def __init__(self, *, value: T) -> None:
        """
        ValueObject value object constructor.

        Args:
            value (T): Value.
        """
        object.__setattr__(self, '_value', value)

    @override
    def __repr__(self) -> str:
        """
        Returns a detailed string representation of the value object.

        Returns:
            str: A string representation of the value object in the format 'ClassName(value=value)'.
        """
        return f'{self.__class__.__name__}(value={self._value!s})'

    @override
    def __str__(self) -> str:
        """
        Returns a simple string representation of the value object.

        Returns:
            str: The string representation of the value object value.
        """
        return str(object=self._value)

    @override
    def __hash__(self) -> int:
        """
        Returns the hash of the value object.

        Returns:
            int: Hash of the value object.
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

    @property
    def value(self) -> T:
        """
        Returns the value object value.

        Returns:
            T: The value object value.
        """
        return self._value
