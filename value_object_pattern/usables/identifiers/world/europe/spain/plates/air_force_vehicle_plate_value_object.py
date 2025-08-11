"""
AirForceVehiclePlateValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class AirForceVehiclePlateValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    AirForceVehiclePlateValueObject value object ensures the provided value is a valid Spanish air force plate. The plate
    format is EA, followed by 4 digits and ending with 3 or 31. It can contain spaces, hyphens, or no separators.

    References:
        Plates: https://matriculasdelmundo.com/espana.html

    Example:
    ```python
    from value_object_pattern.usables.identifiers.world.europe.spain.plates import AirForceVehiclePlateValueObject

    plate = AirForceVehiclePlateValueObject(value='EA-123431')

    print(repr(plate))
    # >>> AirForceVehiclePlateValueObject(value=EA123431)
    ```
    """  # noqa: E501  # fmt: skip

    _VALIDATION_REGEX: Pattern[str] = re_compile(pattern=r'EA[0-9]{4}(3|31)')
    _IDENTIFICATION_REGEX: Pattern[str] = re_compile(pattern=r'([eE][aA])[-\s]?([0-9]{4}[-\s]?(3|31))')

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
            self._raise_value_is_not_air_force_plate(value=value)

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
            self._raise_value_is_not_air_force_plate(value=value)

    def _raise_value_is_not_air_force_plate(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid Spanish air force plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish air force plate.
        """
        raise ValueError(f'AirForceVehiclePlateValueObject value <<<{value}>>> is not a valid Spanish air force plate.')

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
