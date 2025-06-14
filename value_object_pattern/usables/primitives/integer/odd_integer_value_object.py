"""
OddIntegerValueObject value object.
"""

from typing import NoReturn

from value_object_pattern.decorators import validation

from .integer_value_object import IntegerValueObject


class OddIntegerValueObject(IntegerValueObject):
    """
    OddIntegerValueObject value object ensures the provided value is an odd integer.

    Example:
    ```python
    from value_object_pattern.usables import IntegerValueObject

    integer = IntegerValueObject(value=1)

    print(repr(integer))
    # >>> IntegerValueObject(value=1)
    ```
    """

    @validation(order=0)
    def _ensure_value_is_odd_number(self, value: int) -> None:
        """
        Ensures the value object `value` is an odd number.

        Args:
            value (int): The provided value.

        Raises:
            ValueError: If the `value` is not an odd number.
        """
        if value % 2 == 0:
            self._raise_value_is_not_odd_number(value=value)

    def _raise_value_is_not_odd_number(self, value: int) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not an odd number.

        Args:
            value (int): The provided value.

        Raises:
            ValueError: If the `value` is not an odd number.
        """
        raise ValueError(f'OddIntegerValueObject value <<<{value}>>> must be an odd number.')
