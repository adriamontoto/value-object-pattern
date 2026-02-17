"""
SlugValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern.decorators import validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class SlugValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    SlugValueObject ensures the provided value is a valid slug string.
    """

    _VALIDATION_REGEX: Pattern[str] = re_compile(pattern=r'^[a-z0-9]+(?:-[a-z0-9]+)*$')

    @validation(order=0)
    def _ensure_value_follows_validation_regex(self, value: str) -> None:
        """
        Ensures the value object `value` only contains allowed characters.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` contains disallowed characters.
        """
        if not self._VALIDATION_REGEX.fullmatch(string=value):
            self._raise_value_contains_invalid_characters(value=value)

    def _raise_value_contains_invalid_characters(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` contains invalid characters.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` contains invalid characters.
        """
        raise ValueError(f'SlugValueObject value <<<{value}>>> has invalid format. Only lowercase letters and digits separated by single hyphens are allowed.')  # noqa: E501  # fmt: skip
