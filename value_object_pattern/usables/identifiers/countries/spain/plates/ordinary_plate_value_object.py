"""
OrdinaryPlateValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class OrdinaryPlateValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    OrdinaryPlateValueObject value object ensures the provided value is a valid Spanish ordinary plate (2000-today). The
    plate format is 4 digits followed by 3 letters, and can and it can contain spaces, hyphens, or no separators.

    References:
        Plates: https://matriculasdelmundo.com/espana.html

    Example:
    ```python
    from value_object_pattern.usables.identifiers.countries.spain.plates import OrdinaryPlateValueObject

    plate = OrdinaryPlateValueObject(value='1234-BCD')

    print(repr(plate))
    # >>> OrdinaryPlateValueObject(value=1234BCD)
    ```
    """

    __ORDINARY_PLATE_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'([0-9]{4})[-\s]?([bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]{3})')  # noqa: E501  # fmt: skip

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
    def _ensure_value_is_formatted(self, value: str) -> str:
        """
        Ensures the value object `value` is stored in the format 0000BBB.

        Args:
            value (str): The provided value.

        Returns:
            str: Formatted value.
        """
        return self.__ORDINARY_PLATE_VALUE_OBJECT_REGEX.sub(repl=r'\1\2', string=value)

    @validation(order=0)
    def _ensure_value_is_ordinary_plate(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid Spanish ordinary plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish ordinary plate.
        """
        if not self.__ORDINARY_PLATE_VALUE_OBJECT_REGEX.fullmatch(string=value):
            self._raise_value_is_not_ordinary_plate(value=value)

    def _raise_value_is_not_ordinary_plate(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid Spanish ordinary plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish ordinary plate.
        """
        raise ValueError(f'OrdinaryPlateValueObject value <<<{value}>>> is not a valid Spanish ordinary plate.')
