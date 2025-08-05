"""
NavyPlateValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class NavyPlateValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    NavyPlateValueObject value object ensures the provided value is a valid Spanish navy plate. The pate format is FN,
    followed by 4 or 5 digits, and it can contain spaces, hyphens, or no separators.

    References:
        Plates: https://matriculasdelmundo.com/espana.html

    Example:
    ```python
    from value_object_pattern.usables.identifiers.countries.spain.plates import NavyPlateValueObject

    plate = NavyPlateValueObject(value='FN-12345')

    print(repr(plate))
    # >>> NavyPlateValueObject(value=FN-12345)
    ```
    """

    __NAVY_PLATE_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'(fn|FN)[-\s]?([0-9]{4,5})')

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
        Ensures the value object `value` is stored in the format FN-12345.

        Args:
            value (str): The provided value.

        Returns:
            str: Formatted value.
        """
        return self.__NAVY_PLATE_VALUE_OBJECT_REGEX.sub(repl=r'\1\2', string=value)

    @validation(order=0)
    def _ensure_value_is_navy_plate(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid Spanish navy plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish navy plate.
        """
        if not self.__NAVY_PLATE_VALUE_OBJECT_REGEX.fullmatch(string=value):
            self._raise_value_is_not_navy_plate(value=value)

    def _raise_value_is_not_navy_plate(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid Spanish navy plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish navy plate.
        """
        raise ValueError(f'NavyPlateValueObject value <<<{value}>>> is not a valid Spanish navy plate.')
