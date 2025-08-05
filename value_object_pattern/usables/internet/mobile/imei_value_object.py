"""
ImeiValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class ImeiValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    ImeiValueObject value object ensures the provided value is a valid International Mobile Equipment Identity (IMEI).
    An IMEI is a 15-digit numeric string that uniquely identifies a mobile device. It consists of 8 digits Type
    Allocation Code (TAC) identifying the device model and manufacturer, 6 digits Serial Number and 1 digit Check Digit
    calculated using the Luhn algorithm (ISO/IEC 7812).

    Example:
    ```python
    from value_object_pattern.usables.internet.mobile import ImeiValueObject

    imei = ImeiValueObject(value='490154203237518')

    print(repr(imei))
    # >>> ImeiValueObject(value=490154203237518)
    ```
    """

    __IMEI_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'(?:[0-9][\s\-\.]?){14}[0-9]')

    @process(order=0)
    def _ensure_value_has_no_separators(self, value: str) -> str:
        """
        Removes common separators from the IMEI value for processing.

        Args:
            value (str): The provided value.

        Returns:
            str: Value without separators.
        """
        return value.replace('-', '').replace(' ', '').replace('.', '')

    @validation(order=0)
    def _ensure_value_is_imei(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid International Mobile Equipment Identity.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid IMEI.
        """
        if not self.__IMEI_VALUE_OBJECT_REGEX.fullmatch(string=value):
            self._raise_value_is_not_imei(value=value)

        replaced_value = value.replace('-', '').replace(' ', '').replace('.', '')
        if not self._validate_luhn_checksum(imei=replaced_value):
            self._raise_value_is_not_imei(value=value)

    def _validate_luhn_checksum(self, imei: str) -> bool:
        """
        Validates the IMEI using the Luhn algorithm as per ISO/IEC 7812.

        Args:
            imei (str): The IMEI to validate.

        Returns:
            bool: True if checksum is valid.
        """
        digits = [int(digit) for digit in imei]

        # Apply Luhn algorithm, starting from the right, double every other digit, for IMEI, we start from the second
        # to last digit (index 13) going left
        for i in range(13, -1, -2):
            doubled = digits[i] * 2
            if doubled > 9:
                digits[i] = doubled // 10 + doubled % 10

            else:
                digits[i] = doubled

        total = sum(digits)

        return total % 10 == 0

    def _raise_value_is_not_imei(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid IMEI.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid IMEI.
        """
        raise ValueError(f'ImeiValueObject value <<<{value}>>> is not a valid International Mobile Equipment Identity.')
