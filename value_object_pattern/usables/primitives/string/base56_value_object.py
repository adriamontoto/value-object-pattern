"""
Base56StringValueObject value object.
"""

from typing import NoReturn

from value_object_pattern.decorators import validation

from .trimmed_string_value_object import TrimmedStringValueObject


class Base56StringValueObject(TrimmedStringValueObject):
    """
    Ensure the provided value uses the ambiguity-free Base56 alphabet. The empty string is accepted.

    Example:
    ```python
    from value_object_pattern.usables import Base56StringValueObject

    string = Base56StringValueObject(value='5EKAKz6H')

    print(repr(string))
    # >>> Base56StringValueObject(value='5EKAKz6H')
    ```
    """

    __BASE56_ALPHABET: frozenset[str] = frozenset('abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')

    @validation(order=0)
    def _ensure_value_is_base56(self, value: str) -> None:
        """
        Ensure the value uses only Base56 characters.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the value contains a character outside the Base56 alphabet.
        """
        if not set(value).issubset(self.__BASE56_ALPHABET):
            self._raise_value_is_not_base56(value=value)

    def _raise_value_is_not_base56(self, value: str) -> NoReturn:
        """
        Raise a ValueError when the value contains a character outside the Base56 alphabet.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: Always raised because the value contains an invalid character.
        """
        raise ValueError(f'Base56StringValueObject value <<<{value}>>> contains invalid Base56 characters.')
