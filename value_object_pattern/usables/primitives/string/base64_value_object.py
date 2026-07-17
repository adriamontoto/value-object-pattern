"""
Base64StringValueObject value object.
"""

from base64 import b64decode, b64encode
from binascii import Error
from typing import NoReturn

from value_object_pattern.decorators import validation

from .trimmed_string_value_object import TrimmedStringValueObject


class Base64StringValueObject(TrimmedStringValueObject):
    """
    Ensure the provided value is canonical standard Base64. The empty string is accepted as the Base64 encoding of
    empty bytes.

    Example:
    ```python
    from value_object_pattern.usables import Base64StringValueObject

    string = Base64StringValueObject(value='aGVsbG8gd29ybGQ=')

    print(repr(string))
    # >>> Base64StringValueObject(value='aGVsbG8gd29ybGQ=')
    ```
    """

    @validation(order=0)
    def _ensure_value_is_base64(self, value: str) -> None:
        """
        Ensure the value is canonical standard Base64.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the value is not canonical standard Base64.
        """
        try:
            decoded_value = b64decode(s=value, validate=True)

        except (Error, ValueError):
            self._raise_value_is_not_base64(value=value)

        if b64encode(s=decoded_value).decode() != value:
            self._raise_value_is_not_base64(value=value)

    def _raise_value_is_not_base64(self, value: str) -> NoReturn:
        """
        Raise a ValueError when the value is not canonical standard Base64.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: Always raised because the value is not canonical standard Base64.
        """
        raise ValueError(f'Base64StringValueObject value <<<{value}>>> must be canonical standard Base64.')
