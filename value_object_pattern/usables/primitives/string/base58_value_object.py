"""
Base58StringValueObject value object.
"""

from typing import NoReturn

from value_object_pattern.decorators import validation

from .trimmed_string_value_object import TrimmedStringValueObject


class Base58StringValueObject(TrimmedStringValueObject):
    """
    Ensure the provided value uses the Bitcoin Base58 alphabet. The empty string is accepted.

    Example:
    ```python
    from value_object_pattern.usables import Base58StringValueObject

    string = Base58StringValueObject(value='3mJr7AoU')

    print(repr(string))
    # >>> Base58StringValueObject(value='3mJr7AoU')
    ```
    """

    __BASE58_ALPHABET: frozenset[str] = frozenset('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz')

    @validation(order=0)
    def _ensure_value_is_base58(self, value: str) -> None:
        """
        Ensure the value uses only Base58 characters.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the value contains a character outside the Base58 alphabet.
        """
        if not set(value).issubset(self.__BASE58_ALPHABET):
            self._raise_value_is_not_base58(value=value)

    def _raise_value_is_not_base58(self, value: str) -> NoReturn:
        """
        Raise a ValueError when the value contains a character outside the Base58 alphabet.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: Always raised because the value contains an invalid character.
        """
        raise ValueError(f'Base58StringValueObject value <<<{value}>>> contains invalid Base58 characters.')
