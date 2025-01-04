"""
UppercaseStringValueObject value object.
"""

from value_object_pattern.decorators import validation

from .string_value_object import StringValueObject


class UppercaseStringValueObject(StringValueObject):
    """
    UppercaseStringValueObject value object.
    """

    @validation(order=0)
    def ensure_value_is_uppercase(self, value: str) -> None:
        """
        Ensures the value object value is uppercase.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not uppercase.
        """
        if not value.isupper():
            raise ValueError(f'UppercaseStringValueObject value <<<{value}>>> contains lowercase characters. Only uppercase characters are allowed.')  # noqa: E501  # fmt: skip
