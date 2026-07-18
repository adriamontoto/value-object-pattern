"""
Base32StringValueObject value object.
"""

from base64 import b32decode, b32encode
from binascii import Error
from typing import NoReturn

from value_object_pattern.decorators import validation

from .trimmed_string_value_object import TrimmedStringValueObject


class Base32StringValueObject(TrimmedStringValueObject):
    """
    Ensure the provided value is canonical padded Base32. Uppercase and lowercase letters are accepted, as is the empty
    encoding.

    Example:
    ```python
    from value_object_pattern.usables import Base32StringValueObject

    string = Base32StringValueObject(value='NBSWY3DP')

    print(repr(string))
    # >>> Base32StringValueObject(value='NBSWY3DP')
    ```
    """

    @validation(order=0)
    def _ensure_value_is_base32(self, value: str) -> None:
        """
        Ensure the value is canonical padded Base32.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the value is not canonical padded Base32.
        """
        try:
            decoded_value = b32decode(s=value, casefold=True)

        except (Error, ValueError):
            self._raise_value_is_not_base32(value=value)

        if b32encode(s=decoded_value).decode() != value.upper():
            self._raise_value_is_not_base32(value=value)

    def _raise_value_is_not_base32(self, value: str) -> NoReturn:
        """
        Raise a ValueError when the value is not canonical padded Base32.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: Always raised because the value is not canonical padded Base32.
        """
        raise ValueError(f'Base32StringValueObject value <<<{value}>>> must be canonical padded Base32.')
