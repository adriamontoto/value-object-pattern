"""
OrdinaryTruckPlateValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class OrdinaryTruckPlateValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    OrdinaryTruckPlateValueObject value object ensures the provided value is a valid Spanish ordinary truck plate
    (1999-today). The plate format is an R followed by 4 digits followed by 3 letters, and can and it can contain
    spaces, hyphens, or no separators.

    References:
        Plates: https://matriculasdelmundo.com/espana.html

    Example:
    ```python
    from value_object_pattern.usables.identifiers.countries.spain.plates import OrdinaryTruckPlateValueObject

    plate = OrdinaryTruckPlateValueObject(value='R-1234-BCD')

    print(repr(plate))
    # >>> OrdinaryTruckPlateValueObject(value=R1234BCD)
    ```
    """

    __ORDINARY_TRUCK_PLATE_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'([rR])[-\s]?([0-9]{4})[-\s]?([bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]{3})')  # noqa: E501  # fmt: skip

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
        return self.__ORDINARY_TRUCK_PLATE_VALUE_OBJECT_REGEX.sub(repl=r'\1\2\3', string=value)

    @validation(order=0)
    def _ensure_value_is_ordinary_truck_plate(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid Spanish ordinary truck plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish ordinary truck plate.
        """
        if not self.__ORDINARY_TRUCK_PLATE_VALUE_OBJECT_REGEX.fullmatch(string=value):
            self._raise_value_is_not_ordinary_truck_plate(value=value)

    def _raise_value_is_not_ordinary_truck_plate(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid Spanish ordinary truck plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish ordinary truck plate.
        """
        raise ValueError(f'OrdinaryTruckPlateValueObject value <<<{value}>>> is not a valid Spanish ordinary truck plate.')  # noqa: E501  # fmt: skip

    @classmethod
    def regexs(cls) -> list[Pattern[str]]:
        """
        Returns a list of regex patterns used for validation.

        Returns:
            list[Pattern[str]]: List of regex patterns.
        """
        return [cls.__ORDINARY_TRUCK_PLATE_VALUE_OBJECT_REGEX]
