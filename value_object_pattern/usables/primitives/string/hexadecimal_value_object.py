"""
HexadecimalStringValueObject value object.
"""

from re import Pattern, compile as re_compile

from value_object_pattern.decorators import validation

from .string_value_object import StringValueObject


class HexadecimalStringValueObject(StringValueObject):
    """
    HexadecimalStringValueObject value object.

    Example:
    ```python
    from value_object_pattern.usables import HexadecimalStringValueObject

    string = HexadecimalStringValueObject(value='1a2b3c')

    print(repr(string))
    # >>> HexadecimalStringValueObject(value='1a2b3c')
    ```
    """

    __HEXADECIMAL_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'^[0-9a-fA-F]+$')

    @validation(order=0)
    def _ensure_value_is_hexadecimal(self, value: str) -> None:
        """
        Ensures the value object value is hexadecimal.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not hexadecimal.
        """
        if not self.__HEXADECIMAL_VALUE_OBJECT_REGEX.fullmatch(string=value):
            raise ValueError(f'HexadecimalStringValueObject value <<<{value}>>> contains invalid characters. Only hexadecimal characters are allowed.')  # noqa: E501  # fmt: skip
