"""
ScreamingSnakeCaseStringValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import validation

from .non_empty_string_value_object import NotEmptyStringValueObject
from .trimmed_string_value_object import TrimmedStringValueObject


class ScreamingSnakeCaseStringValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    ScreamingSnakeCaseStringValueObject value object ensures the provided value is SCREAMING_SNAKE_CASE.

    Example:
    ```python
    from value_object_pattern.usables import ScreamingSnakeCaseStringValueObject

    string = ScreamingSnakeCaseStringValueObject(value='ABCD_1234')

    print(repr(string))
    # >>> ScreamingSnakeCaseStringValueObject(value='ABCD_1234')
    ```
    """

    _VALIDATION_REGEX: Pattern[str] = re_compile(pattern=r'^[A-Z0-9]+(?:_[A-Z0-9]+)*$')

    @validation(order=0)
    def _ensure_value_is_screaming_snake_case(self, value: str) -> None:
        """
        Ensures the value object `value` is SCREAMING_SNAKE_CASE.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not SCREAMING_SNAKE_CASE.
        """
        if not self._VALIDATION_REGEX.fullmatch(string=value):
            self._raise_value_is_not_screaming_snake_case(value=value)

    def _raise_value_is_not_screaming_snake_case(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not SCREAMING_SNAKE_CASE.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not SCREAMING_SNAKE_CASE.
        """
        raise ValueError(f'ScreamingSnakeCaseStringValueObject value <<<{value}>>> has invalid format. Only uppercase letters and digits separated by single underscores are allowed.')  # noqa: E501  # fmt: skip
