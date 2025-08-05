"""
AgriculturalPlateValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class AgriculturalPlateValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    AgriculturalPlateValueObject value object ensures the provided value is a valid Spanish agricultural vehicle plate.
    The plate format is defined as E initial, followed by four digits and three uppercase letters, it can be represented
    with spaces, hyphens or no separators.

    References:
        Plates: https://matriculasdelmundo.com/espana.html

    Example:
    ```python
    from value_object_pattern.usables.identifiers.countries.spain.plates import AgriculturalPlateValueObject

    plate = AgriculturalPlateValueObject(value='E-1234-ABC')

    print(repr(plate))
    # >>> AgriculturalPlateValueObject(value=E1234ABC)
    ```
    """

    __AGRICULTURAL_PLATE_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'(e|E)[\s-]?([0-9]{4})[\s-]?([A-Za-z]{3})')  # noqa: E501  # fmt: skip

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
        Ensures the value object `value` is stored in the format E-1234-ABC.

        Args:
            value (str): The provided value.

        Returns:
            str: Formatted value.
        """
        return self.__AGRICULTURAL_PLATE_VALUE_OBJECT_REGEX.sub(repl=r'\1\2\3', string=value)

    @validation(order=0)
    def _ensure_value_is_agricultural_plate(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid Spanish agricultural vehicle plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish agricultural vehicle plate.
        """
        if not self.__AGRICULTURAL_PLATE_VALUE_OBJECT_REGEX.fullmatch(string=value):
            self._raise_value_is_not_agricultural_plate(value=value)

    def _raise_value_is_not_agricultural_plate(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid Spanish agricultural vehicle plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish agricultural vehicle plate.
        """
        raise ValueError(f'AgriculturalPlateValueObject value <<<{value}>>> is not a valid Spanish agricultural vehicle plate.')  # noqa: E501  # fmt: skip
