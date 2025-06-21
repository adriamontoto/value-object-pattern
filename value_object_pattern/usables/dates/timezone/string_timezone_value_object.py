"""
StringTimezoneValueObject value object.
"""

from typing import Any, NoReturn
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class StringTimezoneValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    StringTimezoneValueObject value object ensures the provided value is a string timezone.

    Example:
    ```python
    from value_object_pattern.usables.dates import StringTimezoneValueObject

    timezone = StringTimezoneValueObject(value='UTC')

    print(repr(timezone))
    # >>> StringTimezoneValueObject(value='UTC')
    ```
    """

    @process(order=0)
    def _ensure_value_is_normalized(self, value: str) -> str:
        """
        Ensures the value object `value` is normalized timezone string (uppercase).

        Args:
            value (str): The provided value.

        Returns:
            str: The normalized timezone string.
        """
        return value.upper()

    @validation(order=0)
    def _ensure_value_is_timezone(self, value: str) -> None:
        """
        Ensures the value object `value` is a string timezone.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a timezone.
        """
        try:
            ZoneInfo(value)
        except ZoneInfoNotFoundError:
            self._raise_value_is_not_timezone(value=value)

    def _raise_value_is_not_timezone(self, value: Any) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a timezone.

        Args:
            value (Any): The provided value.

        Raises:
            ValueError: If the `value` is not a timezone.
        """
        raise ValueError(f'StringTimezoneValueObject value <<<{value}>>> must be a timezone.')
