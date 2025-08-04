"""
PassportValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class PassportValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    PassportValueObject value object ensures the provided value is a valid Spanish passport.
    A Spanish passport is a string with 9 characters. The first 3 characters are letters
    and the last 6 characters are numbers.

    Example:
    ```python
    from value_object_pattern.usables.identifiers.countries.spain import PassportValueObject

    passport = PassportValueObject(value='ABC123456')

    print(repr(passport))
    # >>> PassportValueObject(value=ABC123456)
    ```
    """

    __PASSPORT_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'([a-zA-Z]{2,3})([0-9]{6})')

    @process(order=0)
    def _ensure_value_is_upper(self, value: str) -> str:
        """
        Ensures the value object `value` is an upper string.

        Args:
            value (str): The provided value.

        Returns:
            str: Upper case value.
        """
        return value.upper()

    @validation(order=0)
    def _ensure_value_is_passport(self, value: str) -> None:
        """
        Ensures the value object `value` is a Spanish passport.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a Spanish passport.
        """
        match = self.__PASSPORT_VALUE_OBJECT_REGEX.fullmatch(string=value)
        if not match:
            self._raise_value_is_not_passport(value=value)

    def _raise_value_is_not_passport(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a Spanish passport.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a Spanish passport.
        """
        raise ValueError(f'PassportValueObject value <<<{value}>>> is not a valid Spanish passport.')
