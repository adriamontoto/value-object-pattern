"""
CivilGuardPlateValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class CivilGuardPlateValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    CivilGuardPlateValueObject value object ensures the provided value is a valid Spanish civil guard plate. The plate
    format is PGC, followed by 5 digits with a final letter identifying the vehicle type, and it can contain spaces,
    hyphens, or no separators.

    References:
        Plates: https://matriculasdelmundo.com/espana.html

    Example:
    ```python
    from value_object_pattern.usables.identifiers.countries.spain.plates import CivilGuardPlateValueObject

    plate = CivilGuardPlateValueObject(value='PGC-12345E')

    print(repr(plate))
    # >>> CivilGuardPlateValueObject(value=PGC12345E)
    ```
    """

    __CIVIL_GUARD_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'(pgc|PGC)[-\s]?([0-9]{5})[-\s]?([a-zA-Z]{1})')  # noqa: E501  # fmt: skip

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
        Ensures the value object `value` is stored in the format PGC12345E.

        Args:
            value (str): The provided value.

        Returns:
            str: Formatted value.
        """
        return self.__CIVIL_GUARD_VALUE_OBJECT_REGEX.sub(repl=r'\1\2\3', string=value)

    @validation(order=0)
    def _ensure_value_is_civil_guard_plate(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid Spanish civil guard plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish civil guard plate.
        """
        if not self.__CIVIL_GUARD_VALUE_OBJECT_REGEX.fullmatch(string=value):
            self._raise_value_is_not_civil_guard_plate(value=value)

    def _raise_value_is_not_civil_guard_plate(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid Spanish civil guard plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish civil guard plate.
        """
        raise ValueError(f'CivilGuardPlateValueObject value <<<{value}>>> is not a valid Spanish civil guard plate.')
