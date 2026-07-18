"""
HexadecimalStringValueObject value object.
"""

from base64 import b16decode
from binascii import Error
from typing import NoReturn

from value_object_pattern.decorators import validation

from .trimmed_string_value_object import TrimmedStringValueObject


class HexadecimalStringValueObject(TrimmedStringValueObject):
    """
    Ensure the provided value is a Base16 string. Uppercase and lowercase hexadecimal letters are accepted, as is the
    empty encoding.

    Example:
    ```python
    from value_object_pattern.usables import HexadecimalStringValueObject

    string = HexadecimalStringValueObject(value='64e9740a')

    print(repr(string))
    # >>> HexadecimalStringValueObject(value='64e9740a')
    ```
    """

    @validation(order=0)
    def _ensure_value_is_hexadecimal(self, value: str) -> None:
        """
        Ensure the value is valid Base16.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the value is not valid Base16.
        """
        try:
            b16decode(s=value, casefold=True)

        except (Error, ValueError):
            self._raise_value_is_not_hexadecimal(value=value)

    def _raise_value_is_not_hexadecimal(self, value: str) -> NoReturn:
        """
        Raise a ValueError when the value is not valid Base16.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: Always raised because the value is not valid Base16.
        """
        raise ValueError(f'HexadecimalStringValueObject value <<<{value}>>> must be valid Base16.')


Base16StringValueObject = HexadecimalStringValueObject
