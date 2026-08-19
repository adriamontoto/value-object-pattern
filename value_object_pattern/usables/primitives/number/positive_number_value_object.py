"""
Provide a positive integer-or-float value object normalized to float.
"""

from typing import NoReturn

from value_object_pattern.decorators import validation

from .number_value_object import NumberValueObject


class PositiveNumberValueObject(NumberValueObject):
    """
    Validate a finite integer or float greater than zero and store it as a float.

    Boolean values are rejected even though `bool` is an `int` subclass. Integer inputs are explicitly converted to
    floats after validation.

    Example:
    ```python
    from value_object_pattern.usables import PositiveNumberValueObject

    quantity = PositiveNumberValueObject(value=2)
    print(repr(quantity))
    # >>> PositiveNumberValueObject(value=2.0)
    ```
    """

    @validation(order=2)
    def _ensure_value_is_positive(self, value: float) -> None:
        """
        Ensure the numeric value is greater than zero.

        Args:
            value (float): The integer or float to validate.

        Raises:
            ValueError: If the value is zero or negative.
        """
        if value <= 0:
            self._raise_value_is_not_positive(value=value)

    def _raise_value_is_not_positive(self, value: float) -> NoReturn:
        """
        Raise an error for a zero or negative number.

        Args:
            value (float): The invalid numeric value.

        Raises:
            ValueError: Always raised with the invalid value.
        """
        raise ValueError(f'PositiveNumberValueObject value <<<{value}>>> must be greater than zero.')
