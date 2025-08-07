"""
AmexValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject
from value_object_pattern.usables.utils import validate_luhn_checksum


class AmexValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    AmexValueObject value object ensures the provided value is a valid American Express credit card number.
    American Express cards start with 34 or 37 and have 15 digits.

    Example:
    ```python
    from value_object_pattern.usables.money.credit_cards import AmexValueObject

    card = AmexValueObject(value='346093248751578')

    print(repr(card))
    # >>> AmexValueObject(value=346093248751578)
    ```
    """

    __AMEX_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'(34|37)((?:[\s\-]*[0-9]){13})')

    @process(order=0)
    def _ensure_value_is_formatted(self, value: str) -> str:
        """
        Ensures the value object `value` is stored without separators.

        Args:
            value (str): The provided value.

        Returns:
            str: Formatted value.
        """
        return ''.join(char for char in value if char.isdigit())

    @validation(order=0)
    def _ensure_value_is_amex_card(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid American Express credit card number.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid American Express credit card number.
        """
        if not self.__AMEX_VALUE_OBJECT_REGEX.fullmatch(string=value):
            self._raise_value_is_not_amex_card(value=value)

        replaced_value = ''.join(char for char in value if char.isdigit())
        if not validate_luhn_checksum(value=replaced_value):
            self._raise_value_is_not_amex_card(value=value)

    def _raise_value_is_not_amex_card(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid American Express credit card number.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid American Express credit card number.
        """
        raise ValueError(f'AmexValueObject value <<<{value}>>> is not a valid American Express credit card number.')

    @classmethod
    def regexs(cls) -> list[Pattern[str]]:
        """
        Returns a list of regex patterns used for validation.

        Returns:
            list[Pattern[str]]: List of regex patterns.
        """
        return [cls.__AMEX_VALUE_OBJECT_REGEX]
