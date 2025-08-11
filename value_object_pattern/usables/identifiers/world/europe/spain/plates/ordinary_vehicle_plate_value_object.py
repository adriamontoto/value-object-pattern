"""
OrdinaryVehiclePlateValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class OrdinaryVehiclePlateValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    OrdinaryVehiclePlateValueObject value object ensures the provided value is a valid Spanish ordinary plate (2000-today). The
    plate format is 4 digits followed by 3 letters, and can and it can contain spaces, hyphens, or no separators.

    References:
        Plates: https://matriculasdelmundo.com/espana.html

    Example:
    ```python
    from value_object_pattern.usables.identifiers.world.europe.spain.plates import OrdinaryVehiclePlateValueObject

    plate = OrdinaryVehiclePlateValueObject(value='1234-BCD')

    print(repr(plate))
    # >>> OrdinaryVehiclePlateValueObject(value=1234BCD)
    ```
    """  # noqa: E501  # fmt: skip

    _VALIDATION_REGEX: Pattern[str] = re_compile(pattern=r'[0-9]{4}[BCDFGHJKLMNPQRSTVWXYZ]{3}')
    _IDENTIFICATION_REGEX: Pattern[str] = re_compile(pattern=r'([0-9]{4})[-\s]?([bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]{3})')  # noqa: E501  # fmt: skip

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
        return self._IDENTIFICATION_REGEX.sub(repl=r'\1\2', string=value)

    @validation(order=0)
    def _ensure_value_follows_identification_regex(self, value: str) -> None:
        """
        Ensures the value object `value` follows the identification regex.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` does not follow the identification regex.
        """
        if not self._IDENTIFICATION_REGEX.fullmatch(string=value):
            self._raise_value_is_not_ordinary_plate(value=value)

    @validation(order=1, early_process=True)
    def _ensure_value_follows_validation_regex(self, value: str, processed_value: str) -> None:
        """
        Ensures the value object `value` follows the validation regex.

        Args:
            value (str): The provided value.
            processed_value (str): The early processed value.

        Raises:
            ValueError: If the `value` does not follow the validation regex.
        """
        if not self._IDENTIFICATION_REGEX.fullmatch(string=processed_value):
            self._raise_value_is_not_ordinary_plate(value=value)

    def _raise_value_is_not_ordinary_plate(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid Spanish ordinary plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish ordinary plate.
        """
        raise ValueError(f'OrdinaryVehiclePlateValueObject value <<<{value}>>> is not a valid Spanish ordinary plate.')

    @classmethod
    def identification_regex(cls) -> Pattern[str]:
        """
        Returns the regex pattern used for identification.

        Returns:
            Pattern[str]: Regex pattern.
        """
        return cls._IDENTIFICATION_REGEX

    @classmethod
    def validation_regex(cls) -> Pattern[str]:
        """
        Returns the regex pattern used for validation.

        Returns:
            Pattern[str]: Regex pattern.
        """
        return cls._VALIDATION_REGEX
