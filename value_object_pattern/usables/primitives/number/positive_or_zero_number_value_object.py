"""
Provide a non-negative integer-or-float value object normalized to float.
"""

from typing import NoReturn

from value_object_pattern.decorators import validation

from .number_value_object import NumberValueObject


class PositiveOrZeroNumberValueObject(NumberValueObject):
    """
    Validate a finite integer or float greater than or equal to zero and store it as a float.

    Boolean values are rejected even though `bool` is an `int` subclass. Integer inputs are explicitly converted to
    floats after validation, and negative zero is normalized to `0.0`.

    Example:
    ```python
    from value_object_pattern.usables import PositiveOrZeroNumberValueObject

    quantity = PositiveOrZeroNumberValueObject(value=0)
    print(repr(quantity))
    # >>> PositiveOrZeroNumberValueObject(value=0.0)
    ```
    """

    @validation(order=2)
    def _ensure_value_is_positive_or_zero(self, value: float) -> None:
        """
        Ensure the numeric value is greater than or equal to zero.

        Args:
            value (float): The integer or float to validate.

        Raises:
            ValueError: If the value is negative.
        """
        if value < 0:
            self._raise_value_is_not_positive_or_zero(value=value)

    def _raise_value_is_not_positive_or_zero(self, value: float) -> NoReturn:
        """
        Raise an error for a negative number.

        Args:
            value (float): The invalid numeric value.

        Raises:
            ValueError: Always raised with the invalid value.
        """
        raise ValueError(f'PositiveOrZeroNumberValueObject value <<<{value}>>> must be greater than or equal to zero.')  # noqa: E501  # fmt: skip
