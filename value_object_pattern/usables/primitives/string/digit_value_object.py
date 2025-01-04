"""
DigitStringValueObject value object.
"""

from value_object_pattern.decorators import validation

from .string_value_object import StringValueObject


class DigitStringValueObject(StringValueObject):
    """
    DigitStringValueObject value object.
    """

    @validation(order=0)
    def ensure_value_is_digit(self, value: str) -> None:
        """
        Ensures the value object value is digit.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not digit.
        """
        if not value.isdigit():
            raise ValueError(f'DigitStringValueObject value <<<{value}>>> contains invalid characters. Only digit characters are allowed.')  # noqa: E501  # fmt: skip
