"""
IbanValueObject value object.
"""

from re import Pattern, compile as re_compile
from string import ascii_uppercase
from typing import ClassVar, NoReturn

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

    _VALIDATION_REGEX: Pattern[str] = re_compile(pattern=r'[A-Z]{2}[0-9]{2}[0-9A-Z]{1,30}')
    _IDENTIFICATION_REGEX: Pattern[str] = re_compile(pattern=r'([a-zA-Z]{2})[\s\-]*([0-9]{2})[\s\-]*([0-9a-zA-Z](?:[\s\-]*[0-9a-zA-Z]){0,29})')  # noqa: E501  # fmt: skip
    _ALPHA_MAP: ClassVar[dict[str, str]] = {character: str(10 + i) for i, character in enumerate(iterable=ascii_uppercase)}  # noqa: E501  # fmt: skip

    @process(order=0)
    def _ensure_value_is_upper(self, value: str) -> str:
        """
        Ensures the value object `value` is stored in upper case.

        Args:
            value (str): The provided value.

        Returns:
            str: Upper case value.
        """
        return value.upper()

    @process(order=1)
    def _ensure_value_is_formatted(self, value: str) -> str:
        """
        Ensures the value object `value` is stored without separators.

        Args:
            value (str): The provided value.

        Returns:
            str: Formatted value.
        """
        return value.replace(' ', '').replace('-', '')

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
            self._raise_value_is_not_iban(value=value)

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
            self._raise_value_is_not_iban(value=value)

    @validation(order=2, early_process=True)
    def _ensure_value_country_code_is_valid(self, value: str, processed_value: str) -> None:
        """
        Ensures the country code is valid.

        Args:
            value (str): The provided value.
            processed_value (str): The early processed value.

        Raises:
            ValueError: If the country code is not valid.
        """
        match = self._IDENTIFICATION_REGEX.fullmatch(string=processed_value)

        country_code, _, _ = match.groups()  # type: ignore[union-attr]
        if country_code not in get_iban_lengths():
            self._raise_value_is_not_iban(value=value)

        expected_length = get_iban_lengths()[country_code]
        if len(processed_value) != expected_length:
            self._raise_value_is_not_iban(value=value)

    @validation(order=3, early_process=True)
    def _ensure_value_follows_mod97_algorithm(self, value: str, processed_value: str) -> None:
        """
        Ensures the value object `value` follows the MOD-97 algorithm.

        Args:
            value (str): The provided value.
            processed_value (str): The early processed value.

        Raises:
            ValueError: If the `value` does not follow the MOD-97 algorithm.
        """
        if not self._validate_mod97_checksum(iban=processed_value):
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
        numeric = ''.join(self._ALPHA_MAP.get(character, character) for character in rearranged)

        return int(numeric) % 97 == 1

    def _raise_value_is_not_iban(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid IBAN.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid IBAN.
        """
        raise ValueError(f'IbanValueObject value <<<{value}>>> is not a valid International Bank Account Number.')

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
