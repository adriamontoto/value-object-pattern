"""
Provide a current ISO 4217 alphabetic currency-code value object.
"""

from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .utils import get_iso4217_alpha3_codes


class CurrencyCodeValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    Validate and normalize a current ISO 4217 three-letter currency or fund code.

    Validation uses ISO 4217 List One as published by the SIX maintenance agency on 2026-01-01. Codes are
    case-insensitive on input and stored in uppercase. Historical codes are not accepted.

    References:
        ISO 4217: https://www.iso.org/iso-4217-currency-codes.html
        SIX List One: https://www.six-group.com/dam/download/financial-information/data-center/iso-currrency/lists/list-one.xml

    Example:
    ```python
    from value_object_pattern.usables.money import CurrencyCodeValueObject

    currency = CurrencyCodeValueObject(value='eur')
    print(repr(currency))
    # >>> CurrencyCodeValueObject(value='EUR')
    ```
    """

    @process(order=0)
    def _normalize_currency_code(self, value: str) -> str:
        """
        Normalize the currency code to uppercase.

        Args:
            value (str): The validated currency code.

        Returns:
            str: The uppercase currency code.
        """
        return value.upper()

    @validation(order=1)
    def _ensure_value_is_currency_code(self, value: str) -> None:
        """
        Ensure the value is a current ISO 4217 alphabetic code.

        Args:
            value (str): The currency code to validate.

        Raises:
            ValueError: If the value is not in the current ISO 4217 catalog.
        """
        if value.upper() not in get_iso4217_alpha3_codes():
            self._raise_value_is_not_currency_code(value=value)

    def _raise_value_is_not_currency_code(self, value: str) -> NoReturn:
        """
        Raise an error for an invalid or historical currency code.

        Args:
            value (str): The invalid currency code.

        Raises:
            ValueError: Always raised with the invalid value.
        """
        raise ValueError(f'CurrencyCodeValueObject value <<<{value}>>> is not a current ISO 4217 currency code.')
