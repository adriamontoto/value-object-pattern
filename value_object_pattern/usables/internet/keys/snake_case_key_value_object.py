"""
SnakeCaseKeyValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class SnakeCaseKeyValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    SnakeCaseKeyValueObject ensures the provided value is a valid snake_case dotted key.

    Example:
    ```python
    from value_object_pattern.usables.internet.keys import SnakeCaseKeyValueObject

    key = SnakeCaseKeyValueObject(value='organization.api_keys.rotate_after_days')

    print(repr(key))
    # >>> SnakeCaseKeyValueObject(value='organization.api_keys.rotate_after_days')
    ```
    """

    _VALIDATION_REGEX: Pattern[str] = re_compile(pattern=r'^[a-z0-9]+(?:_[a-z0-9]+)*(?:\.[a-z0-9]+(?:_[a-z0-9]+)*)*$')

    @validation(order=0)
    def _ensure_value_follows_validation_regex(self, value: str) -> None:
        """
        Ensures the value object `value` follows the snake_case dotted key format.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` has invalid format.
        """
        if not self._VALIDATION_REGEX.fullmatch(string=value):
            self._raise_value_contains_invalid_characters(value=value)

    def _raise_value_contains_invalid_characters(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` contains invalid characters.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` has invalid format.
        """
        raise ValueError(f'SnakeCaseKeyValueObject value <<<{value}>>> has invalid format. Only lowercase letters and digits separated by single underscores inside dot-separated segments are allowed.')  # noqa: E501  # fmt: skip
