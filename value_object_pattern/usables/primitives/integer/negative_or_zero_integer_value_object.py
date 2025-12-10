"""
NegativeOrZeroIntegerValueObject value object.
"""

from typing import NoReturn

from value_object_pattern.decorators import validation

from .integer_value_object import IntegerValueObject


class NegativeOrZeroIntegerValueObject(IntegerValueObject):
    """
    NegativeOrZeroIntegerValueObject value object ensures the provided value is a negative or zero integer.

    Example:
    ```python
    from value_object_pattern.usables import NegativeOrZeroIntegerValueObject

    integer = NegativeOrZeroIntegerValueObject(value=0)

    print(repr(integer))
    # >>> NegativeOrZeroIntegerValueObject(value=0)
    ```
    """

    @validation(order=0)
    def _ensure_value_is_negative_or_zero_integer(self, value: int) -> None:
        """
        Ensures the value object `value` is a negative or zero integer.

        Args:
            value (int): The provided value.

        Raises:
            ValueError: If the `value` is not a negative or zero integer.
        """
        if value > 0:
            self._raise_value_is_not_negative_or_zero_integer(value=value)

    def _raise_value_is_not_negative_or_zero_integer(self, value: int) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a negative or zero integer.

        Args:
            value (int): The provided value.

        Raises:
            ValueError: If the `value` is not a negative or zero integer.
        """
        raise ValueError(f'NegativeOrZeroIntegerValueObject value <<<{value}>>> must be a negative or zero integer.')
