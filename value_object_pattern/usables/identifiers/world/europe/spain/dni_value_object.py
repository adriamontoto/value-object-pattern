"""
DniValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class DniValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    DniValueObject value object ensures the provided value is a valid Spanish DNI.
    A Spanish DNI is a string with 9 characters. The first 8 characters are numbers and the last character is a letter.
    The letter is calculated using the number modulo 23 and the result is compared with a predefined list of letters.

    Example:
    ```python
    from value_object_pattern.usables.identifiers.world.europe.spain import DniValueObject

    dni = DniValueObject(value='87654321X')

    print(repr(dni))
    # >>> DniValueObject(value=87654321X)
    ```
    """

    _DNI_LETTERS: str = 'TRWAGMYFPDXBNJZSQVHLCKE'
    _VALIDATION_REGEX: Pattern[str] = re_compile(pattern=r'[0-9]{8}[TRWAGMYFPDXBNJZSQVHLCKE]')
    _IDENTIFICATION_REGEX: Pattern[str] = re_compile(pattern=r'([0-9]{8})[-\s]?([trwagmyfpdxbnjzsqvhlckeTRWAGMYFPDXBNJZSQVHLCKE])')  # noqa: E501  # fmt: skip

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
        return self._IDENTIFICATION_REGEX.sub(repl=r'\1\2', string=value)

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
            self._raise_value_is_not_dni(value=value)

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
            self._raise_value_is_not_dni(value=value)

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
        number, control_letter = match.groups()  # type: ignore[union-attr]

        expected_letter = self._DNI_LETTERS[int(number) % 23]
        if control_letter != expected_letter:
            self._raise_value_is_not_dni(value=value)

    def _raise_value_is_not_dni(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a Spanish DNI.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a Spanish DNI.
        """
        raise ValueError(f'DniValueObject value <<<{value}>>> is not a valid Spanish DNI.')

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
