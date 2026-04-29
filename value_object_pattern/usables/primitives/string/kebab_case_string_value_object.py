"""
KebabCaseStringValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import validation

from .non_empty_string_value_object import NotEmptyStringValueObject
from .trimmed_string_value_object import TrimmedStringValueObject


class KebabCaseStringValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    KebabCaseStringValueObject value object ensures the provided value is kebab-case.

    Example:
    ```python
    from value_object_pattern.usables import KebabCaseStringValueObject

    string = KebabCaseStringValueObject(value='abcd-1234')

    print(repr(string))
    # >>> KebabCaseStringValueObject(value='abcd-1234')
    ```
    """

    _VALIDATION_REGEX: Pattern[str] = re_compile(pattern=r'^[a-z0-9]+(?:-[a-z0-9]+)*$')

    @validation(order=0)
    def _ensure_value_is_kebab_case(self, value: str) -> None:
        """
        Ensures the value object `value` is kebab-case.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not kebab-case.
        """
        if not self._VALIDATION_REGEX.fullmatch(string=value):
            self._raise_value_is_not_kebab_case(value=value)

    def _raise_value_is_not_kebab_case(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not kebab-case.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not kebab-case.
        """
        raise ValueError(f'KebabCaseStringValueObject value <<<{value}>>> has invalid format. Only lowercase letters and digits separated by single hyphens are allowed.')  # noqa: E501  # fmt: skip
