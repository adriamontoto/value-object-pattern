"""
PositiveOrZeroIntegerValueObject value object.
"""

from typing import NoReturn

from value_object_pattern.decorators import validation

from .integer_value_object import IntegerValueObject


class PositiveOrZeroIntegerValueObject(IntegerValueObject):
    """
    PositiveOrZeroIntegerValueObject value object ensures the provided value is a positive or zero integer.

    Example:
    ```python
    from value_object_pattern.usables import PositiveOrZeroIntegerValueObject

    integer = PositiveOrZeroIntegerValueObject(value=0)

    print(repr(integer))
    # >>> PositiveOrZeroIntegerValueObject(value=0)
    ```
    """

    @validation(order=0)
    def _ensure_value_is_positive_or_zero_integer(self, value: int) -> None:
        """
        Ensures the value object `value` is a positive or zero integer.

        Args:
            value (int): The provided value.

        Raises:
            ValueError: If the `value` is not a positive or zero integer.
        """
        if value < 0:
            self._raise_value_is_not_positive_or_zero_integer(value=value)

    def _raise_value_is_not_positive_or_zero_integer(self, value: int) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a positive or zero integer.

        Args:
            value (int): The provided value.

        Raises:
            ValueError: If the `value` is not a positive or zero integer.
        """
        raise ValueError(f'PositiveOrZeroIntegerValueObject value <<<{value}>>> must be a positive or zero integer.')
