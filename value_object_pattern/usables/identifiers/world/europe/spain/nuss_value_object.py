"""
NussValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .utils import get_provincial_codes


class NussValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    NussValueObject value object ensures the provided value is a valid Spanish Social Security Number (NUSS). A NUSS is
    a string with 11 or 12 digits, structured as 2 digits as province code, followed by 7 or 8 digits as a sequential
    number, and ending with 2 control digits. It can contain spaces, hyphens, forward slashes or no separators.

    Example:
    ```python
    from value_object_pattern.usables.identifiers.world.europe.spain import NussValueObject

    nss = NussValueObject(value='27/76556913/07')

    print(repr(nss))
    # >>> NussValueObject(value=277655691307)
    ```
    """

    _VALIDATION_REGEX: Pattern[str] = re_compile(pattern=r'([0-9]{2})([0-9]{7,8})([0-9]{2})')
    _IDENTIFICATION_REGEX: Pattern[str] = re_compile(pattern=r'([0-9]{2})[-\s/]?([0-9]{7,8})[-\s/]?([0-9]{2})')  # noqa: E501  # fmt: skip

    @process(order=0)
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
            self._raise_value_is_not_social_security_number(value=value)

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
            self._raise_value_is_not_social_security_number(value=value)

    @validation(order=2, early_process=True)
    def _ensure_value_has_valid_province_code(self, value: str, processed_value: str) -> None:
        """
        Ensures the value object `value` has a valid province code.

        Args:
            value (str): The provided value.
            processed_value (str): The early processed value.

        Raises:
            ValueError: If the `value` does not have a valid province code.
        """
        match = self._IDENTIFICATION_REGEX.fullmatch(string=processed_value)

        province, _, _ = match.groups()  # type: ignore[union-attr]
        if int(province) not in get_provincial_codes():
            self._raise_value_is_not_social_security_number(value=value)

    @validation(order=3, early_process=True)
    def _ensure_value_has_valid_control_letter(self, value: str, processed_value: str) -> None:
        """
        Ensures the value object `value` has a valid control letter.

        Args:
            value (str): The provided value.
            processed_value (str): The early processed value.

        Raises:
            ValueError: If the `value` does not have a valid control letter.
        """
        match = self._IDENTIFICATION_REGEX.fullmatch(string=processed_value)
        province, sequential, control = match.groups()  # type: ignore[union-attr]

        expected = self._calculate_control_value(province=province, sequential=sequential)
        if expected != int(control):
            self._raise_value_is_not_social_security_number(value=value)

    def _calculate_control_value(self, province: str, sequential: str) -> int:
        """
        Returns the control digits for the provided province and sequential number.

        Args:
            province (str): The province code (2 digits).
            sequential (str): The sequential number (7-8 digits).

        Returns:
            int: The calculated control value.
        """
        if len(sequential) == 7:
            sequential = f'0{sequential}'

        return int(f'{province}{sequential}') % 97

    def _raise_value_is_not_social_security_number(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid Spanish Social Security Number.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish Social Security Number.
        """
        raise ValueError(f'NussValueObject value <<<{value}>>> is not a valid Spanish Social Security Number.')  # noqa: E501  # fmt: skip

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
