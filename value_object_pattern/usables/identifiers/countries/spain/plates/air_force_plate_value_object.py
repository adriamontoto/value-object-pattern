"""
AirForcePlateValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class AirForcePlateValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    AirForcePlateValueObject value object ensures the provided value is a valid Spanish air force plate. The plate
    format is EA, followed by 4 digits and ending with 3 or 31. It can contain spaces, hyphens, or no separators.

    References:
        Plates: https://matriculasdelmundo.com/espana.html

    Example:
    ```python
    from value_object_pattern.usables.identifiers.countries.spain.plates import AirForcePlateValueObject

    plate = AirForcePlateValueObject(value='EA-123431')

    print(repr(plate))
    # >>> AirForcePlateValueObject(value=EA123431)
    ```
    """

    __AIR_FORCE_PLATE_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'(ea|EA)[-\s]?([0-9]{4}(3|31))')

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
        Ensures the value object `value` is stored in the format EA123456.

        Args:
            value (str): The provided value.

        Returns:
            str: Formatted value.
        """
        return self.__AIR_FORCE_PLATE_VALUE_OBJECT_REGEX.sub(repl=r'\1\2', string=value)

    @validation(order=0)
    def _ensure_value_is_air_force_plate(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid Spanish air force plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish air force plate.
        """
        if not self.__AIR_FORCE_PLATE_VALUE_OBJECT_REGEX.fullmatch(string=value):
            self._raise_value_is_not_air_force_plate(value=value)

    def _raise_value_is_not_air_force_plate(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid Spanish air force plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish air force plate.
        """
        raise ValueError(f'AirForcePlateValueObject value <<<{value}>>> is not a valid Spanish air force plate.')
