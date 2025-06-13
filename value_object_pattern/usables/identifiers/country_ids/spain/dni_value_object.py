"""
DniValueObject value object.
"""

from re import Pattern, compile as re_compile

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class DniValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    DniValueObject value object ensures the provided value is a valid Spanish DNI.
    A Spanish DNI is a string with 9 characters. The first 8 characters are numbers and the last character is a letter.
    The letter is calculated using the number modulo 23 and the result is compared with a predefined list of letters.

    Example:
    ```python
    from value_object_pattern.usables.identifiers.country_ids import DniValueObject

    dni = DniValueObject(value='87654321X')

    print(repr(dni))
    # >>> DniValueObject(value=87654321X)
    ```
    """

    __DNI_VALUE_OBJECT_LETTERS: str = 'TRWAGMYFPDXBNJZSQVHLCKE'
    __DNI_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'([0-9]{8})([a-zA-Z])')

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
    def _ensure_value_is_dni(self, value: str) -> None:
        """
        Ensures the value object `value` is a Spanish DNI.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a Spanish DNI.
        """
        match = self.__DNI_VALUE_OBJECT_REGEX.fullmatch(string=value)
        if not match:
            raise ValueError(f'DniValueObject value <<<{value}>>> is not a valid Spanish DNI.')

        number, letter = match.groups()

        expected_letter = self.__DNI_VALUE_OBJECT_LETTERS[int(number) % 23]
        if letter.upper() != expected_letter:
            raise ValueError(f'DniValueObject value <<<{value}>>> is not a valid Spanish DNI.')
