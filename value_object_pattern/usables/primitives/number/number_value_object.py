"""
Provide shared validation and float normalization for numeric value objects.
"""

from math import isfinite
from typing import Any, NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.models import ValueObject


class NumberValueObject(ValueObject[float]):
    """
    Validate an exact integer or float and store it as a finite float.

    Example:
    ```python
    from value_object_pattern.usables import NumberValueObject

    quantity = NumberValueObject(value=2)
    print(repr(quantity))
    # >>> NumberValueObject(value=2.0)
    ```
    """

    @process(order=0)
    def _normalize_number_to_float(self, value: float) -> float:
        """
        Convert the validated number to its canonical float representation.

        Negative zero is normalized to positive zero.

        Args:
            value (float): The validated integer or float.

        Returns:
            float: The normalized finite float.
        """
        normalized_value = float(value)

        return 0.0 if normalized_value == 0.0 else normalized_value

    @validation(order=0)
    def _ensure_value_is_integer_or_float(self, value: float) -> None:
        """
        Ensure the value is exactly an integer or float.

        Args:
            value (float): The numeric value to validate. Integers are accepted and later normalized to floats.

        Raises:
            TypeError: If the value is not exactly an integer or float.
        """
        if type(value) not in (int, float):
            self._raise_value_is_not_integer_or_float(value=value)

    def _raise_value_is_not_integer_or_float(self, value: Any) -> NoReturn:
        """
        Raise an error for a value that is not an integer or float.

        Args:
            value (Any): The invalid value.

        Raises:
            TypeError: Always raised with the invalid type.
        """
        raise TypeError(f'NumberValueObject value <<<{value}>>> must be an integer or float. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip

    @validation(order=1)
    def _ensure_value_is_finite_float(self, value: float) -> None:
        """
        Ensure the value can be represented as a finite float.

        Args:
            value (float): The integer or float to validate.

        Raises:
            ValueError: If conversion overflows or produces an infinity or NaN.
        """
        try:
            normalized_value = float(value)

        except OverflowError:
            self._raise_value_is_not_finite_float(value=value)

        if not isfinite(normalized_value):
            self._raise_value_is_not_finite_float(value=value)

    def _raise_value_is_not_finite_float(self, value: float) -> NoReturn:
        """
        Raise an error for a value without a finite float representation.

        Args:
            value (float): The invalid numeric value.

        Raises:
            ValueError: Always raised with the invalid value.
        """
        raise ValueError(f'NumberValueObject value <<<{value}>>> must be finite and representable as a float.')  # noqa: E501  # fmt: skip
