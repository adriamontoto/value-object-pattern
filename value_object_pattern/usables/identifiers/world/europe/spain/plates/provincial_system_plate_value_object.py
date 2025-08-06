"""
ProvincialSystemPlateValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .utils import get_provincial_plate_codes


class ProvincialSystemPlateValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    ProvincialSystemPlateValueObject value object ensures the provided value is a valid Spanish provincial system plate
    (1971-2000). The plate format is 1 or 2 letters of province code followed by 4 digits followed with 1 or 2 letters
    and can and it can contain spaces, hyphens, or no separators.

    References:
        Plates: https://matriculasdelmundo.com/espana.html

    Example:
    ```python
    from value_object_pattern.usables.identifiers.world.europe.spain.plates import ProvincialSystemPlateValueObject

    plate = ProvincialSystemPlateValueObject(value='M-0000-A')

    print(repr(plate))
    # >>> ProvincialSystemPlateValueObject(value=M0000A)
    ```
    """  # noqa: E501  # fmt: skip

    __PROVINCIAL_SYSTEM_PLATE_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'([a-zA-Z]{1,2})[-\s]?([0-9]{4})[-\s]?([a-zA-Z]{1,2})')  # noqa: E501  # fmt: skip

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
        return self.__PROVINCIAL_SYSTEM_PLATE_VALUE_OBJECT_REGEX.sub(repl=r'\1\2\3', string=value)

    @validation(order=0)
    def _ensure_value_is_provincial_system_plate(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid Spanish provincial system plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish provincial system plate.
        """
        match = self.__PROVINCIAL_SYSTEM_PLATE_VALUE_OBJECT_REGEX.fullmatch(string=value)
        if not match:
            self._raise_value_is_not_provincial_system_plate(value=value)

        province_code, _, _ = match.groups()
        if province_code.upper() not in get_provincial_plate_codes():
            self._raise_value_is_not_provincial_system_plate(value=value)

    def _raise_value_is_not_provincial_system_plate(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid Spanish provincial system plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish provincial system plate.
        """
        raise ValueError(f'ProvincialSystemPlateValueObject value <<<{value}>>> is not a valid Spanish provincial system plate.')  # noqa: E501  # fmt: skip

    @classmethod
    def regexs(cls) -> list[Pattern[str]]:
        """
        Returns a list of regex patterns used for validation.

        Returns:
            list[Pattern[str]]: List of regex patterns.
        """
        return [cls.__PROVINCIAL_SYSTEM_PLATE_VALUE_OBJECT_REGEX]
