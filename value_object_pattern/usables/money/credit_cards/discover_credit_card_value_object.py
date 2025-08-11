"""
DiscoverCreditCardValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject
from value_object_pattern.usables.utils import validate_luhn_checksum


class DiscoverCreditCardValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    DiscoverCreditCardValueObject value object ensures the provided value is a valid Discover credit card number.
    Discover cards start with 6011, 622126-622925, 644-649, or 65 and have 16-19 digits.

    Example:
    ```python
    from value_object_pattern.usables.money.credit_cards import DiscoverCreditCardValueObject

    card = DiscoverCreditCardValueObject(value='6011442769137926')

    print(repr(card))
    # >>> DiscoverCreditCardValueObject(value=6011442769137926)
    ```
    """

    _VALIDATION_REGEX: Pattern[str] = re_compile(pattern=r'(?:6011|622(?:1(?:2[6-9]|[3-9][0-9])|[2-8][0-9]{2}|9(?:[01][0-9]|2[0-5]))|64[4-9]|65)[0-9]{10,13}')  # noqa: E501  # fmt: skip
    _IDENTIFICATION_REGEX: Pattern[str] = re_compile(pattern=r'(?:6011|622(?:1(?:2[6-9]|[3-9][0-9])|[2-8][0-9]{2}|9(?:[01][0-9]|2[0-5]))|64[4-9]|65)(?:[\s-]?[0-9]){10,13}')  # noqa: E501  # fmt: skip

    @process(order=0)
    def _ensure_value_is_formatted(self, value: str) -> str:
        """
        Ensures the value object `value` is stored without separators.

        Args:
            value (str): The provided value.

        Returns:
            str: Formatted value.
        """
        return ''.join(character for character in value if character.isdigit())

    @validation(order=0)
    def _ensure_value_follows_identification_regex(self, value: str) -> None:
        """
        Ensures the value object `value` follows the identification regex.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` does not follow the identification regex.
        """
        if not self._IDENTIFICATION_REGEX.fullmatch(string=value):
            self._raise_value_is_not_discover_credit_card(value=value)

    @validation(order=1, early_process=True)
    def _ensure_value_follows_validation_regex(self, value: str, processed_value: str) -> None:
        """
        Ensures the value object `value` follows the validation regex.

        Args:
            value (str): The provided value.
            processed_value (str): The early processed value.

        Raises:
            ValueError: If the `value` does not follow the validation regex.
        """
        if not self._IDENTIFICATION_REGEX.fullmatch(string=processed_value):
            self._raise_value_is_not_discover_credit_card(value=value)

    @validation(order=2, early_process=True)
    def _ensure_value_follows_luhn_algorithm(self, value: str, processed_value: str) -> None:
        """
        Ensures the value object `value` follows the Luhn algorithm.

        Args:
            value (str): The provided value.
            processed_value (str): The early processed value.

        Raises:
            ValueError: If the `value` does not follow the Luhn algorithm.
        """
        if not validate_luhn_checksum(value=processed_value):
            self._raise_value_is_not_discover_credit_card(value=value)

    def _raise_value_is_not_discover_credit_card(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid Discover credit card number.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Discover credit card number.
        """
        raise ValueError(f'DiscoverCreditCardValueObject value <<<{value}>>> is not a valid Discover credit card number.')  # noqa: E501  # fmt: skip

    @classmethod
    def identification_regex(cls) -> Pattern[str]:
        """
        Returns the regex pattern used for identification.

        Returns:
            Pattern[str]: Regex pattern.
        """
        return cls._IDENTIFICATION_REGEX

    @classmethod
    def validation_regex(cls) -> Pattern[str]:
        """
        Returns the regex pattern used for validation.

        Returns:
            Pattern[str]: Regex pattern.
        """
        return cls._VALIDATION_REGEX
