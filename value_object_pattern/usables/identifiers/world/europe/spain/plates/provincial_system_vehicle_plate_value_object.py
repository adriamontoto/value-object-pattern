"""
ProvincialSystemVehiclePlateValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .utils import get_provincial_plate_codes


class ProvincialSystemVehiclePlateValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    ProvincialSystemVehiclePlateValueObject value object ensures the provided value is a valid Spanish provincial system plate
    (1971-2000). The plate format is 1 or 2 letters of province code followed by 4 digits followed with 1 or 2 letters
    and can and it can contain spaces, hyphens, or no separators.

    References:
        Plates: https://matriculasdelmundo.com/espana.html

    Example:
    ```python
    from value_object_pattern.usables.identifiers.world.europe.spain.plates import ProvincialSystemVehiclePlateValueObject

    plate = ProvincialSystemVehiclePlateValueObject(value='M-0000-A')

    print(repr(plate))
    # >>> ProvincialSystemVehiclePlateValueObject(value=M0000A)
    ```
    """  # noqa: E501  # fmt: skip

    _VALIDATION_REGEX: Pattern[str] = re_compile(pattern=r'[A-Z]{1,2}[0-9]{4}[A-Z]{1,2}')
    _IDENTIFICATION_REGEX: Pattern[str] = re_compile(pattern=r'([a-zA-Z]{1,2})[-\s]?([0-9]{4})[-\s]?([a-zA-Z]{1,2})')  # noqa: E501  # fmt: skip

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
        return self._IDENTIFICATION_REGEX.sub(repl=r'\1\2\3', string=value)

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
            self._raise_value_is_not_provincial_system_plate(value=value)

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
            self._raise_value_is_not_provincial_system_plate(value=value)

    @validation(order=2, early_process=True)
    def _ensure_value_has_invalid_provincial_code(self, value: str, processed_value: str) -> None:
        """
        Ensures the value object `value` has an invalid provincial code.

        Args:
            value (str): The provided value.
            processed_value (str): The early processed value.

        Raises:
            ValueError: If the `value` has an invalid provincial code.
        """
        match = self._IDENTIFICATION_REGEX.fullmatch(string=value)

        province_code, _, _ = match.groups()  # type: ignore[union-attr]
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
        raise ValueError(f'ProvincialSystemVehiclePlateValueObject value <<<{value}>>> is not a valid Spanish provincial system plate.')  # noqa: E501  # fmt: skip

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
