"""
AlphanumericStringValueObject value object.
"""

from value_object_pattern.decorators import validation

from .string_value_object import StringValueObject


class AlphanumericStringValueObject(StringValueObject):
    """
    AlphanumericStringValueObject value object.
    """

    @validation(order=0)
    def ensure_value_is_alphanumeric(self, value: str) -> None:
        """
        Ensures the value object value is alphanumeric.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not alphanumeric.
        """
        if not value.isalnum():
            raise ValueError(f'AlphanumericStringValueObject value <<<{value}>>> contains invalid characters. Only alphanumeric characters are allowed.')  # noqa: E501  # fmt: skip
