"""
Provide a canonical ULID string value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class UlidValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    Validate and normalize a canonical Universally Unique Lexicographically Sortable Identifier.

    ULIDs contain 26 case-insensitive Crockford Base32 characters. The letters `I`, `L`, `O`, and `U` are excluded,
    and the first character is restricted to `0` through `7` so the encoded value does not exceed 128 bits. Valid
    values are stored in uppercase.

    References:
        ULID specification: https://github.com/ulid/spec

    Example:
    ```python
    from value_object_pattern.usables.identifiers import UlidValueObject

    identifier = UlidValueObject(value='01arz3ndektsv4rrffq69g5fav')
    print(repr(identifier))
    # >>> UlidValueObject(value='01ARZ3NDEKTSV4RRFFQ69G5FAV')
    ```
    """

    _ULID_REGEX: Pattern[str] = re_compile(r'^[0-7][0-9A-HJKMNP-TV-Z]{25}$')

    @process(order=0)
    def _normalize_ulid(self, value: str) -> str:
        """
        Normalize the ULID to uppercase.

        Args:
            value (str): The validated ULID string.

        Returns:
            str: The uppercase ULID string.
        """
        return value.upper()

    @validation(order=1)
    def _ensure_value_is_ulid(self, value: str) -> None:
        """
        Ensure the value is a canonical 128-bit ULID string.

        Args:
            value (str): The ULID string to validate.

        Raises:
            ValueError: If the value is not a canonical ULID.
        """
        if self._ULID_REGEX.fullmatch(string=value.upper()) is None:
            self._raise_value_is_not_ulid(value=value)

    def _raise_value_is_not_ulid(self, value: str) -> NoReturn:
        """
        Raise an error for an invalid ULID string.

        Args:
            value (str): The invalid ULID string.

        Raises:
            ValueError: Always raised with the invalid value.
        """
        raise ValueError(f'UlidValueObject value <<<{value}>>> is not a valid ULID.')
