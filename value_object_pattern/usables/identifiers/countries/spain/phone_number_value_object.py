"""
PhoneNumberValueObject value object.
"""

from re import Pattern, compile as re_compile, sub
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class PhoneNumberValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    PhoneNumberValueObject value object ensures the provided value is a valid Spanish phone number. A Spanish phone
    number can be a mobile number (starting with 6 or 7) or a landline number (starting with 8 or 9). It can include the
    country code +34 or 0043 or none, and can have spaces, dashes, or no separators.

    Valid formats:
    - Mobile: (+34|0034) 6XX XXX XXX, (+34|0034) 7XX XXX XXX
    - Landline: (+34|0034) 8XX XXX XXX, (+34|0034) 9XX XXX XXX
    - Separators: spaces, dashes, or none

    Example:
    ```python
    from value_object_pattern.usables.identifiers.countries.spain import PhoneNumberValueObject

    phone = PhoneNumberValueObject(value='+34 612 345 678')

    print(repr(phone))
    # >>> PhoneNumberValueObject(value=+34612345678)
    ```
    """

    __PHONE_NUMBER_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'(?:\+34|0034)?[\s\-\(\)]*([6789](?:[\s\-\(\)]*[0-9]){8})')  # noqa: E501  # fmt: skip

    @process(order=0)
    def _normalize_phone_number(self, value: str) -> str:
        """
        Normalizes the phone number by removing spaces, dashes, and ensuring +34 prefix.

        Args:
            value (str): The provided value.

        Returns:
            str: Normalized phone number.
        """
        value = sub(pattern=r'[ \-\(\)]', repl='', string=value)

        if value.startswith('+34'):
            pass  # already canonical

        elif value.startswith('0034'):
            value = '+34' + value[4:]

        elif value.startswith('34'):
            value = '+34' + value[2:]

        else:
            value = '+34' + value

        return value

    @validation(order=0)
    def _ensure_value_is_spanish_phone_number(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid Spanish phone number.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish phone number.
        """
        if not self.__PHONE_NUMBER_VALUE_OBJECT_REGEX.fullmatch(string=value):
            self._raise_value_is_not_spanish_phone_number(value=value)

    def _raise_value_is_not_spanish_phone_number(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid Spanish phone number.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish phone number.
        """
        raise ValueError(f'PhoneNumberValueObject value <<<{value}>>> is not a valid Spanish phone number.')
