"""
CatalanPolicePlateValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class CatalanPolicePlateValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    CatalanPolicePlateValueObject value object ensures the provided value is a valid Spanish Catalan police plate. The
    plate format is CME, followed by 4 numbers and it can contain spaces, hyphens, or no separators.

    References:
        Plates: https://matriculasdelmundo.com/espana.html

    Example:
    ```python
    from value_object_pattern.usables.identifiers.countries.spain.plates import CatalanPolicePlateValueObject

    plate = CatalanPolicePlateValueObject(value='CME-1234')

    print(repr(plate))
    # >>> CatalanPolicePlateValueObject(value=CME1234)
    ```
    """

    __CATALAN_POLICE_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'(cme|CME)[\s-]?([0-9]{4})')

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
        Ensures the value object `value` is stored in the format CME1234.

        Args:
            value (str): The provided value.

        Returns:
            str: Formatted value.
        """
        return self.__CATALAN_POLICE_VALUE_OBJECT_REGEX.sub(repl=r'\1\2', string=value)

    @validation(order=0)
    def _ensure_value_is_police_plate(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid Spanish Catalan police plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish Catalan police plate.
        """
        if not self.__CATALAN_POLICE_VALUE_OBJECT_REGEX.fullmatch(string=value):
            self._raise_value_is_not_police_plate(value=value)

    def _raise_value_is_not_police_plate(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid Spanish Catalan police plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish Catalan police plate.
        """
        raise ValueError(f'CatalanPolicePlateValueObject value <<<{value}>>> is not a valid Spanish Catalan police plate.')  # noqa: E501  # fmt: skip
