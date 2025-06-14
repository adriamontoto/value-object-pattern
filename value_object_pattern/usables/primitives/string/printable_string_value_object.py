"""
PrintableStringValueObject value object.
"""

from typing import NoReturn

from value_object_pattern.decorators import validation

from .string_value_object import StringValueObject


class PrintableStringValueObject(StringValueObject):
    """
    PrintableStringValueObject value object ensures the provided value is printable.

    Example:
    ```python
    from value_object_pattern.usables import PrintableStringValueObject

    string = PrintableStringValueObject(value='abcd1234')

    print(repr(string))
    # >>> PrintableStringValueObject(value='abcd1234')
    ```
    """

    @validation(order=0)
    def _ensure_value_is_printable(self, value: str) -> None:
        """
        Ensures the value object `value` is printable.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not printable.
        """
        if not value.isprintable():
            self._raise_value_is_not_printable(value=value)

    def _raise_value_is_not_printable(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not printable.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not printable.
        """
        raise ValueError(f'PrintableStringValueObject value <<<{value}>>> contains invalid characters. Only printable characters are allowed.')  # noqa: E501  # fmt: skip
