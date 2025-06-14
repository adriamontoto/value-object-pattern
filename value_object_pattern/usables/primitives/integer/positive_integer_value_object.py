"""
PositiveIntegerValueObject value object.
"""

from typing import NoReturn

from value_object_pattern.decorators import validation

from .integer_value_object import IntegerValueObject


class PositiveIntegerValueObject(IntegerValueObject):
    """
    PositiveIntegerValueObject value object ensures the provided value is a positive integer.

    Example:
    ```python
    from value_object_pattern.usables import PositiveIntegerValueObject

    integer = PositiveIntegerValueObject(value=1)

    print(repr(integer))
    # >>> PositiveIntegerValueObject(value=1)
    ```
    """

    @validation(order=0)
    def _ensure_value_is_positive_integer(self, value: int) -> None:
        """
        Ensures the value object `value` is a positive integer.

        Args:
            value (int): The provided value.

        Raises:
            ValueError: If the `value` is not a positive integer.
        """
        if value <= 0:
            self._raise_value_is_not_positive_integer(value=value)

    def _raise_value_is_not_positive_integer(self, value: int) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a positive integer.

        Args:
            value (int): The provided value.

        Raises:
            ValueError: If the `value` is not a positive integer.
        """
        raise ValueError(f'PositiveIntegerValueObject value <<<{value}>>> must be a positive integer.')
