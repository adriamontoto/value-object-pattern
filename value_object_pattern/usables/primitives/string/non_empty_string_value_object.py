"""
NotEmptyStringValueObject value object.
"""

from value_object_pattern.decorators import validation

from .string_value_object import StringValueObject


class NotEmptyStringValueObject(StringValueObject):
    """
    NotEmptyStringValueObject value object.
    """

    @validation(order=0)
    def _ensure_value_is_not_empty_string(self, value: str) -> None:
        """
        Ensures the value object value is not an empty string.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is an empty string.
        """
        if not value:
            raise ValueError(f'NotEmptyStringValueObject value <<<{value}>>> is an empty string. Only non-empty strings are allowed.')  # noqa: E501  # fmt: skip
