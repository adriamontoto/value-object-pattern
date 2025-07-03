"""
IterableValueObject module.
"""

from collections.abc import Iterable
from typing import Any, NoReturn

from value_object_pattern.decorators import validation
from value_object_pattern.models.value_object import ValueObject


class IterableValueObject(ValueObject[Iterable[Any]]):
    """
    IterableValueObject is a value object that ensures the provided value is from an iterable.

    Example:
    ```python
    from value_object_pattern.models.collections import IterableValueObject

    iterable = IterableValueObject(value=[1, 2, 3])
    print(iterable)
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
        from value_object_pattern.models.collections import IterableValueObject

        iterable = IterableValueObject(value=[1, 2, 3])
        print(1 in iterable)
        # >>> True
        ```
        """
        return item in self._value

    @validation(order=0)
    def _ensure_value_is_from_iterable(self, value: Iterable[Any]) -> None:
        """
        Ensures the value object `value` is an iterable.

        Args:
            value (Iterable[Any]): The provided value.

        Raises:
            TypeError: If the `value` is not an iterable.
        """
        if not isinstance(value, Iterable):
            self._raise_value_is_not_iterable(value=value)

    def _raise_value_is_not_iterable(self, value: Any) -> NoReturn:
        """
        Raises a TypeError if the value object `value` is not an iterable.

        Args:
            value (Any): The provided value.

        Raises:
            TypeError: If the `value` is not an iterable.
        """
        raise TypeError(f'IterableValueObject value <<<{value}>>> must be an iterable. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip
