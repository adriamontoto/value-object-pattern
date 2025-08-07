"""
VisaValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject
from value_object_pattern.usables.utils import validate_luhn_checksum


class VisaValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    VisaValueObject value object ensures the provided value is a valid Visa credit card number. Visa cards start with
    4 and have 13, 16, or 19 digits.

    Example:
    ```python
    from value_object_pattern.usables.money.credit_cards import VisaValueObject

    card = VisaValueObject(value='4408040603838265')

    print(repr(card))
    # >>> VisaValueObject(value=4408040603838265)
    ```
    """

    __VISA_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'(4)((?:[\s-]*[0-9]){12}|(?:[\s-]*[0-9]){15}|(?:[\s-]*[0-9]){18})')  # noqa: E501  # fmt: skip

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
    def _ensure_value_is_visa_card(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid Visa credit card number.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Visa credit card number.
        """
        if not self.__VISA_VALUE_OBJECT_REGEX.fullmatch(string=value):
            self._raise_value_is_not_visa_card(value=value)

        replaced_value = ''.join(char for char in value if char.isdigit())
        if not validate_luhn_checksum(value=replaced_value):
            self._raise_value_is_not_visa_card(value=value)

    def _raise_value_is_not_visa_card(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid Visa credit card number.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Visa credit card number.
        """
        raise ValueError(f'VisaValueObject value <<<{value}>>> is not a valid Visa credit card number.')

    @classmethod
    def regexs(cls) -> list[Pattern[str]]:
        """
        Returns a list of regex patterns used for validation.

        Returns:
            list[Pattern[str]]: List of regex patterns.
        """
        return [cls.__VISA_VALUE_OBJECT_REGEX]
