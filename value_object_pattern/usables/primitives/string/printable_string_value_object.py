"""
PrintableStringValueObject value object.
"""

from value_object_pattern.decorators import validation

from .string_value_object import StringValueObject


class PrintableStringValueObject(StringValueObject):
    """
    PrintableStringValueObject value object.
    """

    @validation(order=0)
    def ensure_value_is_printable(self, value: str) -> None:
        """
        Ensures the value object value is printable.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not printable.
        """
        if not value.isprintable():
            raise ValueError(f'PrintableStringValueObject value <<<{value}>>> contains invalid characters. Only printable characters are allowed.')  # noqa: E501  # fmt: skip
