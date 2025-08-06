"""
AdministrativeTechnicianPlateValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class AdministrativeTechnicianPlateValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    AdministrativeTechnicianPlateValueObject value object ensures the provided value is a valid Spanish administrative
    technician plate. The plate format is TA, followed by 3 digits (not all mandatory) and ending with 3 digits. It can
    contain spaces, hyphens, or no separators.

    References:
        Plates: https://matriculasdelmundo.com/espana.html

    Example:
    ```python
    from value_object_pattern.usables.identifiers.countries.spain.plates import AdministrativeTechnicianPlateValueObject

    plate = AdministrativeTechnicianPlateValueObject(value='TA-123-456')

    print(repr(plate))
    # >>> AdministrativeTechnicianPlateValueObject(value=TA123456)
    ```
    """

    __ADMINISTRATIVE_TECHNICIAN_PLATE_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'([tT][aA])[-\s]?([0-9]{1,3})[-\s]?([0-9]{3})')  # noqa: E501  # fmt: skip

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
        return self.__ADMINISTRATIVE_TECHNICIAN_PLATE_VALUE_OBJECT_REGEX.sub(repl=r'\1\2\3', string=value)

    @validation(order=0)
    def _ensure_value_is_administrative_technician_plate(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid Spanish administrative technician plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish administrative technician plate.
        """
        if not self.__ADMINISTRATIVE_TECHNICIAN_PLATE_VALUE_OBJECT_REGEX.fullmatch(string=value):
            self._raise_value_is_not_administrative_technician_plate(value=value)

    def _raise_value_is_not_administrative_technician_plate(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid Spanish administrative technician plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish administrative technician plate.
        """
        raise ValueError(f'AdministrativeTechnicianPlateValueObject value <<<{value}>>> is not a valid Spanish administrative technician plate.')  # noqa: E501  # fmt: skip

    @classmethod
    def regexs(cls) -> list[Pattern[str]]:
        """
        Returns a list of regex patterns used for validation.

        Returns:
            list[Pattern[str]]: List of regex patterns.
        """
        return [cls.__ADMINISTRATIVE_TECHNICIAN_PLATE_VALUE_OBJECT_REGEX]
