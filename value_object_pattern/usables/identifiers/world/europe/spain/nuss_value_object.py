"""
NussValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


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

    __SOCIAL_SECURITY_NUMBER_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'([0-9]{2})[-\s/]?([0-9]{7,8})[-\s/]?([0-9]{2})')  # noqa: E501  # fmt: skip

    @process(order=0)
    def _ensure_value_is_formatted(self, value: str) -> str:
        """
        Ensures the value object `value` is stored without separators.

        Args:
            value (str): The provided value.

        Returns:
            str: Formatted value.
        """
        return self.__SOCIAL_SECURITY_NUMBER_VALUE_OBJECT_REGEX.sub(repl=r'\1\2\3', string=value)

    @validation(order=0)
    def _ensure_value_is_social_security_number(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid Spanish Social Security Number.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish Social Security Number.
        """
        match = self.__SOCIAL_SECURITY_NUMBER_VALUE_OBJECT_REGEX.fullmatch(string=value)
        if not match:
            self._raise_value_is_not_social_security_number(value=value)

        province, sequential, control = match.groups()

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
