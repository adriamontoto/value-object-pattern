"""
AlphabeticStringValueObject value object.
"""

from value_object_pattern.decorators import validation

from .string_value_object import StringValueObject


class AlphabeticStringValueObject(StringValueObject):
    """
    AlphabeticStringValueObject value object.
    """

    @validation(order=0)
    def _ensure_value_is_alphabetic(self, value: str) -> None:
        """
        Ensures the value object value is alphabetic.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not alphabetic.
        """
        if not value.isalpha():
            raise ValueError(f'AlphabeticStringValueObject value <<<{value}>>> contains invalid characters. Only alphabetic characters are allowed.')  # noqa: E501  # fmt: skip
