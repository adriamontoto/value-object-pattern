"""
NationalPolicePlateValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class NationalPolicePlateValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    NationalPolicePlateValueObject value object ensures the provided value is a valid Spanish national police plate.
    The plate format is CNP, followed by 4 numbers and 2 letters, the first number and the first letter identifies the
    vehicle type and it can contain spaces, hyphens, or no separators.

    References:
        Plates: https://matriculasdelmundo.com/espana.html

    Example:
    ```python
    from value_object_pattern.usables.identifiers.countries.spain.plates import NationalPolicePlateValueObject

    plate = NationalPolicePlateValueObject(value='CNP-1234-AA')

    print(repr(plate))
    # >>> NationalPolicePlateValueObject(value=CNP1234AA)
    ```
    """

    __NATIONAL_POLICE_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'(cnp|CNP)[\s-]?([0-9]{4})[\s-]?([a-zA-Z]{2})')  # noqa: E501  # fmt: skip

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
        Ensures the value object `value` is stored in the format CNP1234AA.

        Args:
            value (str): The provided value.

        Returns:
            str: Formatted value.
        """
        return self.__NATIONAL_POLICE_VALUE_OBJECT_REGEX.sub(repl=r'\1\2\3', string=value)

    @validation(order=0)
    def _ensure_value_is_police_plate(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid Spanish police plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish police plate.
        """
        if not self.__NATIONAL_POLICE_VALUE_OBJECT_REGEX.fullmatch(string=value):
            self._raise_value_is_not_police_plate(value=value)

    def _raise_value_is_not_police_plate(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid Spanish police plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish police plate.
        """
        raise ValueError(f'NationalPolicePlateValueObject value <<<{value}>>> is not a valid Spanish police plate.')
