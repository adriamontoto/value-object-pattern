"""
TrimmedStringValueObject value object.
"""

from value_object_pattern.decorators import validation

from .string_value_object import StringValueObject


class TrimmedStringValueObject(StringValueObject):
    """
    TrimmedStringValueObject value object.
    """

    @validation(order=0)
    def _ensure_value_is_trimmed(self, value: str) -> None:
        """
        Ensures the value object value is trimmed.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not trimmed.
        """
        if value != value.strip():
            raise ValueError(f'TrimmedStringValueObject value <<<{value}>>> contains leading or trailing whitespaces. Only trimmed values are allowed.')  # noqa: E501  # fmt: skip
