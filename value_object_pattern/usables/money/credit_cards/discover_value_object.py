"""
DiscoverValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject
from value_object_pattern.usables.utils import validate_luhn_checksum


class DiscoverValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    DiscoverValueObject value object ensures the provided value is a valid Discover credit card number.
    Discover cards start with 6011, 622126-622925, 644-649, or 65 and have 16-19 digits.

    Example:
    ```python
    from value_object_pattern.usables.money.credit_cards import DiscoverValueObject

    card = DiscoverValueObject(value='6011442769137926')

    print(repr(card))
    # >>> DiscoverValueObject(value=6011442769137926)
    ```
    """

    __DISCOVER_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'(?:6011|622(?:1(?:2[6-9]|[3-9][0-9])|[2-8][0-9]{2}|9(?:[01][0-9]|2[0-5]))|64[4-9]|65)(?:[\s-]?\d){10,13}')  # noqa: E501  # fmt: skip

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
    def _ensure_value_is_discover_card(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid Discover credit card number.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Discover credit card number.
        """
        if not self.__DISCOVER_VALUE_OBJECT_REGEX.fullmatch(string=value):
            self._raise_value_is_not_discover_card(value=value)

        replaced_value = ''.join(char for char in value if char.isdigit())
        if not validate_luhn_checksum(value=replaced_value):
            self._raise_value_is_not_discover_card(value=value)

    def _raise_value_is_not_discover_card(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid Discover credit card number.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Discover credit card number.
        """
        raise ValueError(f'DiscoverValueObject value <<<{value}>>> is not a valid Discover credit card number.')

    @classmethod
    def regexs(cls) -> list[Pattern[str]]:
        """
        Returns a list of regex patterns used for validation.

        Returns:
            list[Pattern[str]]: List of regex patterns.
        """
        return [cls.__DISCOVER_VALUE_OBJECT_REGEX]
