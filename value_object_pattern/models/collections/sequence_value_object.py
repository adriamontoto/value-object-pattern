"""
SequenceValueObject module.
"""

from collections.abc import Iterator, Sequence
from typing import Any, NoReturn

from value_object_pattern.decorators import validation
from value_object_pattern.models.value_object import ValueObject


class SequenceValueObject(ValueObject[Sequence[Any]]):
    """
    SequenceValueObject is a value object that ensures the provided value is from a sequence.

    Example:
    ```python
    from value_object_pattern.models.collections import SequenceValueObject

    sequence = SequenceValueObject(value=[1, 2, 3])
    print(sequence)
    # >>> [1, 2, 3]
    ```
    """

    def __contains__(self, item: Any) -> bool:
        """
        Returns True if the value object value contains the item, otherwise False.

        Args:
            item (Any): The item to check.

        Returns:
            bool: True if the value object value contains the item, otherwise False.

        Example:
        ```python
        from value_object_pattern.models.collections import SequenceValueObject

        sequence = SequenceValueObject(value=[1, 2, 3])
        print(1 in sequence)
        # >>> True
        ```
        """
        return item in self._value

    def __iter__(self) -> Iterator[Any]:
        """
        Returns an iterator over the value object value.

        Returns:
            Iterator[Any]: An iterator over the value object value.

        Example:
        ```python
        from value_object_pattern.models.collections import SequenceValueObject

        sequence = SequenceValueObject(value=[1, 2, 3])
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
        from value_object_pattern.models.collections import SequenceValueObject

        sequence = SequenceValueObject(value=[1, 2, 3])
        print(len(sequence))
        # >>> 3
        ```
        """
        return len(self._value)

    def __reversed__(self) -> Iterator[Any]:
        """
        Returns a reversed iterator over the value object value.

        Returns:
            Iterator[Any]: A reversed iterator over the value object value.

        Example:
        ```python
        from value_object_pattern.models.collections import SequenceValueObject

        sequence = SequenceValueObject(value=[1, 2, 3])
        print(list(reversed(sequence)))
        # >>> [3, 2, 1]
        ```
        """
        return reversed(self._value)

    @validation(order=0)
    def _ensure_value_is_from_sequence(self, value: Sequence[Any]) -> None:
        """
        Ensures the value object `value` is a sequence.

        Args:
            value (Sequence[Any]): The provided value.

        Raises:
            TypeError: If the `value` is not a sequence.
        """
        if not isinstance(value, Sequence):
            self._raise_value_is_not_sequence(value=value)

    def _raise_value_is_not_sequence(self, value: Any) -> NoReturn:
        """
        Raises a TypeError if the value object `value` is not a sequence.

        Args:
            value (Any): The provided value.

        Raises:
            TypeError: If the `value` is not a sequence.
        """
        raise TypeError(f'SequenceValueObject value <<<{value}>>> must be a sequence. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip

    def is_empty(self) -> bool:
        """
        Returns True if the value object value is empty, otherwise False.

        Returns:
            bool: True if the value object value is empty, otherwise False.

        Example:
        ```python
        from value_object_pattern.models.collections import SequenceValueObject

        sequence = SequenceValueObject(value=[])
        print(sequence.is_empty())
        # >>> True
        ```
        """
        return not self._value
