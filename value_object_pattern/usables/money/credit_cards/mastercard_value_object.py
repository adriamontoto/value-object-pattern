"""
MasterCardValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject
from value_object_pattern.usables.utils import validate_luhn_checksum


class MasterCardValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    MasterCardValueObject value object ensures the provided value is a valid MasterCard credit card number.
    MasterCard cards start with 5 (51-55) or 2 (2221-2720) and have 16 digits.

    Example:
    ```python
    from value_object_pattern.usables.money.credit_cards import MasterCardValueObject

    card = MasterCardValueObject(value='5189876610072287')

    print(repr(card))
    # >>> MasterCardValueObject(value=5189876610072287)
    ```
    """

    __MASTERCARD_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'(?:5[1-5](?:[\s-]?[0-9]{2}){7}|(?:222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)(?:[\s-]?[0-9]{2}){6})')  # noqa: E501  # fmt: skip

    @process(order=9)
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
    def _ensure_value_is_mastercard(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid MasterCard credit card number.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid MasterCard credit card number.
        """
        if not self.__MASTERCARD_VALUE_OBJECT_REGEX.fullmatch(string=value):
            self._raise_value_is_not_mastercard(value=value)

        replaced_value = ''.join(char for char in value if char.isdigit())
        if not validate_luhn_checksum(value=replaced_value):
            self._raise_value_is_not_mastercard(value=value)

    def _raise_value_is_not_mastercard(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid MasterCard credit card number.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid MasterCard credit card number.
        """
        raise ValueError(f'MasterCardValueObject value <<<{value}>>> is not a valid MasterCard credit card number.')

    @classmethod
    def regexs(cls) -> list[Pattern[str]]:
        """
        Returns a list of regex patterns used for validation.

        Returns:
            list[Pattern[str]]: List of regex patterns.
        """
        return [cls.__MASTERCARD_VALUE_OBJECT_REGEX]
