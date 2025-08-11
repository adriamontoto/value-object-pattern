"""
VisaCreditCardValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject
from value_object_pattern.usables.utils import validate_luhn_checksum


class VisaCreditCardValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    VisaCreditCardValueObject value object ensures the provided value is a valid Visa credit card number. Visa cards
    start with 4 and have 13, 16, or 19 digits.

    Example:
    ```python
    from value_object_pattern.usables.money.credit_cards import VisaCreditCardValueObject

    card = VisaCreditCardValueObject(value='4408040603838265')

    print(repr(card))
    # >>> VisaCreditCardValueObject(value=4408040603838265)
    ```
    """

    _VALIDATION_REGEX: Pattern[str] = re_compile(pattern=r'4[0-9]{12}|4[0-9]{15}|4[0-9]{18}')
    _IDENTIFICATION_REGEX: Pattern[str] = re_compile(pattern=r'(4)((?:[\s-]*[0-9]){12}|(?:[\s-]*[0-9]){15}|(?:[\s-]*[0-9]){18})')  # noqa: E501  # fmt: skip

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
            self._raise_value_is_not_visa_credit_card(value=value)

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
            self._raise_value_is_not_visa_credit_card(value=value)

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
            self._raise_value_is_not_visa_credit_card(value=value)

    def _raise_value_is_not_visa_credit_card(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid Visa credit card number.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Visa credit card number.
        """
        raise ValueError(f'VisaCreditCardValueObject value <<<{value}>>> is not a valid Visa credit card number.')

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
