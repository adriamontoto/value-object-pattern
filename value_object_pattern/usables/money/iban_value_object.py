"""
IbanValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .utils import get_iban_lengths


class IbanValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    IbanValueObject value object ensures the provided value is a valid International Bank Account Number (IBAN). An
    IBAN is an alphanumeric string up to 34 characters long that uniquely identifies a bank account across national
    borders. It consists of 2 letters ISO 3166-1 alpha-2 country code, 2 check digits calculated using MOD-97 algorithm
    (ISO 7064) and up to 30 alphanumeric characters for the Basic Bank Account Number (BBAN).

    Example:
    ```python
    from value_object_pattern.usables.money import IbanValueObject

    iban = IbanValueObject(value='GB82WEST12345698765432')

    print(repr(iban))
    # >>> IbanValueObject(value=GB82WEST12345698765432)
    ```
    """

    __IBAN_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'([a-zA-Z]{2})[\s\-]*([0-9]{2})[\s\-]*([a-zA-Z0-9](?:[\s\-]*[a-zA-Z0-9]){0,29})')  # noqa: E501  # fmt: skip

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

    @process(order=1)
    def _ensure_value_has_separators(self, value: str) -> str:
        """
        Removes all separators (spaces and hyphens) from the IBAN value for processing.

        Args:
            value (str): The provided value.

        Returns:
            str: Value without spaces and hyphens.
        """
        return value.replace(' ', '').replace('-', '')

    @validation(order=0)
    def _ensure_value_is_iban(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid International Bank Account Number.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid IBAN.
        """
        match = self.__IBAN_VALUE_OBJECT_REGEX.fullmatch(string=value)
        if not match:
            self._raise_value_is_not_iban(value=value)

        replaced_value = value.upper().replace(' ', '').replace('-', '')
        country_code, _, _ = match.groups()
        if country_code not in get_iban_lengths():
            self._raise_value_is_not_iban(value=value)

        expected_length = get_iban_lengths()[country_code]
        if len(replaced_value) != expected_length:
            self._raise_value_is_not_iban(value=value)

        if not self._validate_mod97_checksum(iban=replaced_value):
            self._raise_value_is_not_iban(value=value)

    def _validate_mod97_checksum(self, iban: str) -> bool:
        """
        Validates the IBAN using MOD-97 algorithm as per ISO 7064.

        Args:
            iban (str): The IBAN to validate.

        Returns:
            bool: True if checksum is valid.
        """
        rearranged = iban[4:] + iban[:4]

        numeric_string = ''
        for character in rearranged:
            if character.isdigit():
                numeric_string += character

            else:
                numeric_string += str(ord(character) - ord('A') + 10)

        return self._calculate_mod97(numeric_string=numeric_string) == 1

    def _calculate_mod97(self, numeric_string: str) -> int:
        """
        Calculates MOD-97 for large numbers by processing in chunks.

        Args:
            numeric_string (str): The numeric string to process.

        Returns:
            int: The remainder after MOD-97 operation.
        """
        remainder = 0

        i = 0
        while i < len(numeric_string):
            if remainder < 10:  # noqa: SIM108
                chunk_size = min(8, len(numeric_string) - i)

            else:
                chunk_size = min(7, len(numeric_string) - i)

            chunk = str(remainder) + numeric_string[i : i + chunk_size]
            remainder = int(chunk) % 97
            i += chunk_size

        return remainder

    def _raise_value_is_not_iban(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid IBAN.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid IBAN.
        """
        raise ValueError(f'IbanValueObject value <<<{value}>>> is not a valid International Bank Account Number.')
