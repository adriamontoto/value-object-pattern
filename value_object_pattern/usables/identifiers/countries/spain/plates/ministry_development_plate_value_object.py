"""
MinistryDevelopmentPlateValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class MinistryDevelopmentPlateValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    MinistryDevelopmentPlateValueObject value object ensures the provided value is a valid Spanish ministry of
    development plate. The plate format is MMA followed by 5 numbers and it can contain spaces, hyphens, or no
    separators.

    References:
        Plates: https://matriculasdelmundo.com/espana.html

    Example:
    ```python
    from value_object_pattern.usables.identifiers.countries.spain.plates import MinistryDevelopmentPlateValueObject

    plate = MinistryDevelopmentPlateValueObject(value='MMA-12345')

    print(repr(plate))
    # >>> MinistryDevelopmentPlateValueObject(value=MMA12345)
    ```
    """

    __MINISTRY_DEVELOPMENT_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'([mM][mM][aA])[\s-]?([0-9]{5})[\s-]?([a-zA-Z])')  # noqa: E501  # fmt: skip

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
        return self.__MINISTRY_DEVELOPMENT_VALUE_OBJECT_REGEX.sub(repl=r'\1\2\3', string=value)

    @validation(order=0)
    def _ensure_value_is_ministry_development_plate(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid Spanish ministry of development plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish ministry of development plate.
        """
        if not self.__MINISTRY_DEVELOPMENT_VALUE_OBJECT_REGEX.fullmatch(string=value):
            self._raise_value_is_not_ministry_development_plate(value=value)

    def _raise_value_is_not_ministry_development_plate(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid Spanish ministry of development plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish ministry of development plate.
        """
        raise ValueError(f'MinistryDevelopmentPlateValueObject value <<<{value}>>> is not a valid Spanish ministry of development plate.')  # noqa: E501  # fmt: skip

    @classmethod
    def regexs(cls) -> list[Pattern[str]]:
        """
        Returns a list of regex patterns used for validation.

        Returns:
            list[Pattern[str]]: List of regex patterns.
        """
        return [cls.__MINISTRY_DEVELOPMENT_VALUE_OBJECT_REGEX]
