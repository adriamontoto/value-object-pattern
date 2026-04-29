"""
PascalCaseStringValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import validation

from .non_empty_string_value_object import NotEmptyStringValueObject
from .trimmed_string_value_object import TrimmedStringValueObject


class PascalCaseStringValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    PascalCaseStringValueObject value object ensures the provided value is PascalCase.

    Example:
    ```python
    from value_object_pattern.usables import PascalCaseStringValueObject

    string = PascalCaseStringValueObject(value='Abcd1234Word')

    print(repr(string))
    # >>> PascalCaseStringValueObject(value='Abcd1234Word')
    ```
    """

    _VALIDATION_REGEX: Pattern[str] = re_compile(pattern=r'^[A-Z][a-z0-9]*(?:[A-Z][a-z0-9]*)*$')

    @validation(order=0)
    def _ensure_value_is_pascal_case(self, value: str) -> None:
        """
        Ensures the value object `value` is PascalCase.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not PascalCase.
        """
        if not self._VALIDATION_REGEX.fullmatch(string=value):
            self._raise_value_is_not_pascal_case(value=value)

    def _raise_value_is_not_pascal_case(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is PascalCase.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not PascalCase.
        """
        raise ValueError(f'PascalCaseStringValueObject value <<<{value}>>> has invalid format. Only PascalCase strings starting with an uppercase letter and continuing with alphanumeric words are allowed.')  # noqa: E501  # fmt: skip
