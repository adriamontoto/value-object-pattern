"""
CanariasPolicePlateValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class CanariasPolicePlateValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    CanariasPolicePlateValueObject value object ensures the provided value is a valid Spanish Canarias police plate.
    The plate format is CGPC followed by 4 numbers and it can contain spaces, hyphens, or no separators.

    References:
        Plates: https://matriculasdelmundo.com/espana.html

    Example:
    ```python
    from value_object_pattern.usables.identifiers.world.europe.spain.plates import CanariasPolicePlateValueObject

    plate = CanariasPolicePlateValueObject(value='CGPC-1234')

    print(repr(plate))
    # >>> CanariasPolicePlateValueObject(value=CGPC1234)
    ```
    """  # noqa: E501  # fmt: skip

    __CANARIAS_POLICE_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'([cC][gG][pP][cC])[\s-]?([0-9]{4})')  # noqa: E501  # fmt: skip

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
        return self.__CANARIAS_POLICE_VALUE_OBJECT_REGEX.sub(repl=r'\1\2\3', string=value)

    @validation(order=0)
    def _ensure_value_is_canarias_police_plate(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid Spanish Canarias police plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish Canarias police plate.
        """
        if not self.__CANARIAS_POLICE_VALUE_OBJECT_REGEX.fullmatch(string=value):
            self._raise_value_is_not_canarias_police_plate(value=value)

    def _raise_value_is_not_canarias_police_plate(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid Spanish Canarias police plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish Canarias police plate.
        """
        raise ValueError(f'CanariasPolicePlateValueObject value <<<{value}>>> is not a valid Spanish Canarias police plate.')  # noqa: E501  # fmt: skip

    @classmethod
    def regexs(cls) -> list[Pattern[str]]:
        """
        Returns a list of regex patterns used for validation.

        Returns:
            list[Pattern[str]]: List of regex patterns.
        """
        return [cls.__CANARIAS_POLICE_VALUE_OBJECT_REGEX]
