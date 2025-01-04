"""
LowercaseStringValueObject value object.
"""

from value_object_pattern.decorators import validation

from .string_value_object import StringValueObject


class LowercaseStringValueObject(StringValueObject):
    """
    LowercaseStringValueObject value object.
    """

    @validation(order=0)
    def ensure_value_is_lowercase(self, value: str) -> None:
        """
        Ensures the value object value is lowercase.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not lowercase.
        """
        if not value.islower():
            raise ValueError(f'LowercaseStringValueObject value <<<{value}>>> contains uppercase characters. Only lowercase characters are allowed.')  # noqa: E501  # fmt: skip
