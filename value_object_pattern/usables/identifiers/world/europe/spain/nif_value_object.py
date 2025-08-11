"""
NifValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import ClassVar, NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class NifValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    NifValueObject value object ensures the provided value is a valid Spanish company NIF, formerly known as CIF.
    A Spanish company NIF is a string with 9 characters. The first character is a letter that indicates the entity type,
    the next 7 characters are numbers, and the last character is a control character (letter or number) calculated
    using a specific algorithm.

    Example:
    ```python
    from value_object_pattern.usables.identifiers.world.europe.spain import NifValueObject

    nif = NifValueObject(value='A58818501')

    print(repr(nif))
    # >>> NifValueObject(value=A58818501)
    ```
    """

    _NIF_LETTER_CONTROL_LETTERS: ClassVar[list[str]] = ['J', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    _NIF_CONTROL_CHARACTER_LETTERS: ClassVar[set[str]] = {'K', 'P', 'Q', 'S'}
    _NIF_CONTROL_CHARACTER_DIGITS: ClassVar[set[str]] = {'A', 'B', 'E', 'H'}
    _VALIDATION_REGEX: Pattern[str] = re_compile(pattern=r'[ABCDEFGHJNPQRSUVW][0-9]{7}[0-9ABCDEFGHIJ]')
    _IDENTIFICATION_REGEX: Pattern[str] = re_compile(pattern=r'([abcdefghjnpqrsuvwABCDEFGHJNPQRSUVW])[-\s]?([0-9]{7})[-\s]?([0-9abcdefghijABCDEFGHIJ])')  # noqa: E501  # fmt: skip

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
        return self._IDENTIFICATION_REGEX.sub(repl=r'\1\2\3', string=value)

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
            self._raise_value_is_not_nif(value=value)

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
            self._raise_value_is_not_nif(value=value)

    @validation(order=2, early_process=True)
    def _ensure_value_has_valid_control_letter(self, value: str, processed_value: str) -> None:
        """
        Ensures the value object `value` has a valid control letter.

        Args:
            value (str): The provided value.
            processed_value (str): The early processed value.

        Raises:
            ValueError: If the `value` does not have a valid control letter.
        """
        match = self._IDENTIFICATION_REGEX.fullmatch(string=processed_value)
        first_letter, number, control_character = match.groups()  # type: ignore[union-attr]

        expected_number, expected_letter = self._calculate_control_values(number=number)
        if first_letter.upper() in self._NIF_CONTROL_CHARACTER_DIGITS:
            expected = {expected_number}

        elif first_letter.upper() in self._NIF_CONTROL_CHARACTER_LETTERS:
            expected = {expected_letter}

        else:
            expected = {expected_number, expected_letter}

        if control_character.upper() not in expected:
            self._raise_value_is_not_nif(value=value)

    def _calculate_control_values(self, number: str) -> tuple[str, str]:
        """
        Calculates the control character for a Spanish company NIF.

        Args:
            number (str): The 7-digit number part of the NIF.

        Returns:
            tuple[str, str]: The calculated control digit and letter.
        """
        total = 0
        for idx, digit in enumerate(iterable=number):
            n = int(digit)
            if idx % 2 == 0:
                n *= 2
                if n >= 10:
                    n = n // 10 + n % 10

            total += n

        control_value = (10 - (total % 10)) % 10

        return str(control_value), self._NIF_LETTER_CONTROL_LETTERS[control_value]

    def _raise_value_is_not_nif(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a Spanish company NIF.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a Spanish company NIF.
        """
        raise ValueError(f'NifValueObject value <<<{value}>>> is not a valid Spanish company NIF.')

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
