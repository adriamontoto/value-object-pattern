"""
PhoneNumberValueObject value object.
"""

from re import Pattern, compile as re_compile, sub
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject
from value_object_pattern.usables.identifiers.world import PhoneCodeValueObject


class PhoneNumberValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    PhoneNumberValueObject value object ensures the provided value is a valid Spanish phone number. A Spanish phone
    number can be a mobile number (starting with 6 or 7) or a landline number (starting with 8 or 9). It can include the
    country code +34 or 0043 or none, and can have spaces, hyphens, or no separators.

    Valid formats:
    - Mobile: (+34|0034) 6XX XXX XXX, (+34|0034) 7XX XXX XXX
    - Landline: (+34|0034) 8XX XXX XXX, (+34|0034) 9XX XXX XXX
    - Separators: spaces, hyphens, or none

    Example:
    ```python
    from value_object_pattern.usables.identifiers.world.europe.spain import PhoneNumberValueObject

    phone = PhoneNumberValueObject(value='+34 612 345 678')

    print(repr(phone))
    # >>> PhoneNumberValueObject(value=+34612345678)
    ```
    """

    _VALIDATION_REGEX: Pattern[str] = re_compile(pattern=r'(?:34|\+34|0034)?(\s)?[6789][0-9]{8}')
    _IDENTIFICATION_REGEX: Pattern[str] = re_compile(pattern=r'(?:34|\+34|0034)?[\s-]?([6789](?:[\s-]?[0-9]){8})')  # noqa: E501  # fmt: skip

    @process(order=1)
    def _ensure_value_is_formatted(self, value: str) -> str:
        """
        Ensures the value object `value` is stored without separators.

        Args:
            value (str): The provided value.

        Returns:
            str: Formatted value.
        """
        value = sub(pattern=r'[\s-]', repl='', string=value)

        if value.startswith('34'):
            return f'34 {value[2:]}'

        if value.startswith('0034'):
            return f'34 {value[4:]}'

        if value.startswith('+34'):
            return f'34 {value[3:]}'

        return f'34 {value}'

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
            self._raise_value_is_not_spanish_phone_number(value=value)

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

    @property
    def phone_code(self) -> PhoneCodeValueObject:
        """
        Returns the phone code of the phone number.

        Returns:
            PhoneCodeValueObject: The phone code of the phone number.
        """
        return PhoneCodeValueObject(value=self.value.split()[0])
