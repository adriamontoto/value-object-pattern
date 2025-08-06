"""
StateMotorPoolPlateValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class StateMotorPoolPlateValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    StateMotorPoolPlateValueObject value object ensures the provided value is a valid Spanish state motor pool plate.
    The plate format is PME followed by 4 numbers and 1 letter and it can contain spaces, hyphens, or no separators.

    References:
        Plates: https://matriculasdelmundo.com/espana.html

    Example:
    ```python
    from value_object_pattern.usables.identifiers.countries.spain.plates import StateMotorPoolPlateValueObject

    plate = StateMotorPoolPlateValueObject(value='PME-1234-A')

    print(repr(plate))
    # >>> StateMotorPoolPlateValueObject(value=PME1234A)
    ```
    """

    __STATE_MOTOR_POOL_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'([pP][mM][eE])[\s-]?([0-9]{4})[\s-]?([a-zA-Z])')  # noqa: E501  # fmt: skip

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
        return self.__STATE_MOTOR_POOL_VALUE_OBJECT_REGEX.sub(repl=r'\1\2\3', string=value)

    @validation(order=0)
    def _ensure_value_is_state_motor_pool_plate(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid Spanish state motor pool plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish state motor pool plate.
        """
        if not self.__STATE_MOTOR_POOL_VALUE_OBJECT_REGEX.fullmatch(string=value):
            self._raise_value_is_not_state_motor_pool_plate(value=value)

    def _raise_value_is_not_state_motor_pool_plate(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid Spanish state motor pool plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish state motor pool plate.
        """
        raise ValueError(f'StateMotorPoolPlateValueObject value <<<{value}>>> is not a valid Spanish state motor pool plate.')  # noqa: E501  # fmt: skip

    @classmethod
    def regexs(cls) -> list[Pattern[str]]:
        """
        Returns a list of regex patterns used for validation.

        Returns:
            list[Pattern[str]]: List of regex patterns.
        """
        return [cls.__STATE_MOTOR_POOL_VALUE_OBJECT_REGEX]
