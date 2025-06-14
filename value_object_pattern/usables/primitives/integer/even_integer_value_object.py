"""
EvenIntegerValueObject value object.
"""

from typing import NoReturn

from value_object_pattern.decorators import validation

from .integer_value_object import IntegerValueObject


class EvenIntegerValueObject(IntegerValueObject):
    """
    EvenIntegerValueObject value object ensures the provided value is an even integer.

    Example:
    ```python
    from value_object_pattern.usables import EvenIntegerValueObject

    integer = EvenIntegerValueObject(value=2)

    print(repr(integer))
    # >>> EvenIntegerValueObject(value=2)
    ```
    """

    @validation(order=0)
    def _ensure_value_is_even_number(self, value: int) -> None:
        """
        Ensures the value object `value` is an even number.

        Args:
            value (int): The provided value.

        Raises:
            ValueError: If the `value` is not an even number.
        """
        if value % 2 != 0:
            self._raise_value_is_not_even_number(value=value)

    def _raise_value_is_not_even_number(self, value: int) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not an even number.

        Args:
            value (int): The provided value.

        Raises:
            ValueError: If the `value` is not an even number.
        """
        raise ValueError(f'EvenIntegerValueObject value <<<{value}>>> must be an even number.')
