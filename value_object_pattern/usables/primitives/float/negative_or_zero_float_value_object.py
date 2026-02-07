"""
NegativeOrZeroFloatValueObject value object.
"""

from typing import NoReturn

from value_object_pattern.decorators import validation

from .float_value_object import FloatValueObject


class NegativeOrZeroFloatValueObject(FloatValueObject):
    """
    NegativeOrZeroFloatValueObject value object ensures the provided value is a negative or zero float.

    Example:
    ```python
    from value_object_pattern.usables import NegativeOrZeroFloatValueObject

    float_ = NegativeOrZeroFloatValueObject(value=0.0)

    print(repr(float_))
    # >>> NegativeOrZeroFloatValueObject(value=0.0)
    ```
    """

    @validation(order=0)
    def _ensure_value_is_negative_or_zero_float(self, value: float) -> None:
        """
        Ensures the value object `value` is a negative or zero float.

        Args:
            value (float): The provided value.

        Raises:
            ValueError: If the `value` is not a negative or zero float.
        """
        if value > 0:
            self._raise_value_is_not_negative_or_zero_float(value=value)

    def _raise_value_is_not_negative_or_zero_float(self, value: float) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a negative or zero float.

        Args:
            value (float): The provided value.

        Raises:
            ValueError: If the `value` is not a negative or zero float.
        """
        raise ValueError(f'NegativeOrZeroFloatValueObject value <<<{value}>>> must be a negative or zero float.')
