"""
NieValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import ClassVar, NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class NieValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    NieValueObject value object ensures the provided value is a valid Spanish NIE.
    A Spanish NIE is a string with 9 characters. The first character is X, Y, or Z, the next 7 characters are numbers,
    and the last character is a letter. The letter is calculated using the number modulo 23 and the result is compared
    with a predefined list of letters.

    Example:
    ```python
    from value_object_pattern.usables.identifiers.countries.spain import NieValueObject

    nie = NieValueObject(value='X1234567L')

    print(repr(nie))
    # >>> NieValueObject(value=X1234567L)
    ```
    """

    __NIE_VALUE_OBJECT_LETTERS: str = 'TRWAGMYFPDXBNJZSQVHLCKE'
    __NIE_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'([xyzXYZ])([0-9]{7})([trwagmyfpdxbnjzsqvhlckeTRWAGMYFPDXBNJZSQVHLCKE])')  # noqa: E501  # fmt: skip
    __NIE_VALUE_OBJECT_LETTER_TO_NUMBER: ClassVar[dict[str, str]] = {'X': '0', 'Y': '1', 'Z': '2'}

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

    @validation(order=0)
    def _ensure_value_is_nie(self, value: str) -> None:
        """
        Ensures the value object `value` is a Spanish NIE.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a Spanish NIE.
        """
        match = self.__NIE_VALUE_OBJECT_REGEX.fullmatch(string=value)
        if not match:
            self._raise_value_is_not_nie(value=value)

        first_letter, number, control_letter = match.groups()

        expected_letter = self._calculate_control_value(first_letter=first_letter, number=number)
        if control_letter.upper() != expected_letter:
            self._raise_value_is_not_nie(value=value)

    def _calculate_control_value(self, first_letter: str, number: str) -> str:
        """
        Calculates the control letter for a given NIE.

        Args:
            first_letter (str): The first letter of the NIE (X, Y, or Z).
            number (str): The 7-digit number part of the NIE.

        Returns:
            str: The expected control letter.
        """
        number_for_calculation = self.__NIE_VALUE_OBJECT_LETTER_TO_NUMBER[first_letter] + number
        return self.__NIE_VALUE_OBJECT_LETTERS[int(number_for_calculation) % 23]

    def _raise_value_is_not_nie(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a Spanish NIE.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a Spanish NIE.
        """
        raise ValueError(f'NieValueObject value <<<{value}>>> is not a valid Spanish NIE.')
