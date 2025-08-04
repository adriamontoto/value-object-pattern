"""
VinValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class VinValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    VinValueObject value object ensures the provided value is a valid Vehicle Identification Number (VIN). A VIN is a
    17 character string that uniquely identifies a motor vehicle. It uses only capital letters (excluding I, O, and Q to
    avoid confusion with numbers) and digits (0-9).

    Example:
    ```python
    from value_object_pattern.usables.identifiers.countries import VinValueObject

    vin = VinValueObject(value='1HGBH41JXMN109186')

    print(repr(vin))
    # >>> VinValueObject(value=1HGBH41JXMN109186)
    ```
    """

    __VIN_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'[abcdefghjklmnprstuvwxyzABCDEFGHJKLMNPRSTUVWXYZ0-9]{17}')  # noqa: E501  # fmt: skip

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

    @validation(order=0)
    def _ensure_value_is_vin(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid Vehicle Identification Number.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid VIN.
        """
        if not self.__VIN_VALUE_OBJECT_REGEX.fullmatch(string=value):
            self._raise_value_is_not_vin(value=value)

    def _raise_value_is_not_vin(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid VIN.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid VIN.
        """
        raise ValueError(f'VinValueObject value <<<{value}>>> is not a valid Vehicle Identification Number.')
