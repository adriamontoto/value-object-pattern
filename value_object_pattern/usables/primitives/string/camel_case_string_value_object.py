"""
CamelCaseStringValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import validation

from .non_empty_string_value_object import NotEmptyStringValueObject
from .trimmed_string_value_object import TrimmedStringValueObject


class CamelCaseStringValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    CamelCaseStringValueObject value object ensures the provided value is camelCase.

    Example:
    ```python
    from value_object_pattern.usables import CamelCaseStringValueObject

    string = CamelCaseStringValueObject(value='abcd1234Word')

    print(repr(string))
    # >>> CamelCaseStringValueObject(value='abcd1234Word')
    ```
    """

    _VALIDATION_REGEX: Pattern[str] = re_compile(pattern=r'^[a-z][a-z0-9]*(?:[A-Z][a-z0-9]*)*$')

    @validation(order=0)
    def _ensure_value_is_camel_case(self, value: str) -> None:
        """
        Ensures the value object `value` is camelCase.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not camelCase.
        """
        if not self._VALIDATION_REGEX.fullmatch(string=value):
            self._raise_value_is_not_camel_case(value=value)

    def _raise_value_is_not_camel_case(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not camelCase.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not camelCase.
        """
        raise ValueError(f'CamelCaseStringValueObject value <<<{value}>>> has invalid format. Only camelCase strings starting with a lowercase letter and continuing with alphanumeric words are allowed.')  # noqa: E501  # fmt: skip
