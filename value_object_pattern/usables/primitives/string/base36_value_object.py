"""
Base36StringValueObject value object.
"""

from typing import NoReturn

from value_object_pattern.decorators import validation

from .trimmed_string_value_object import TrimmedStringValueObject


class Base36StringValueObject(TrimmedStringValueObject):
    """
    Ensure the provided value uses the uppercase Base36 alphabet. The empty string is accepted.

    Example:
    ```python
    from value_object_pattern.usables import Base36StringValueObject

    string = Base36StringValueObject(value='HELLO123')

    print(repr(string))
    # >>> Base36StringValueObject(value='HELLO123')
    ```
    """

    __BASE36_ALPHABET: frozenset[str] = frozenset('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    @validation(order=0)
    def _ensure_value_is_base36(self, value: str) -> None:
        """
        Ensure the value uses only Base36 characters.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the value contains a character outside the Base36 alphabet.
        """
        if not set(value).issubset(self.__BASE36_ALPHABET):
            self._raise_value_is_not_base36(value=value)

    def _raise_value_is_not_base36(self, value: str) -> NoReturn:
        """
        Raise a ValueError when the value contains a character outside the Base36 alphabet.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: Always raised because the value contains an invalid character.
        """
        raise ValueError(f'Base36StringValueObject value <<<{value}>>> contains invalid Base36 characters.')
