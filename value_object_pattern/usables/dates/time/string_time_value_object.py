"""
Provide a normalized ISO 8601 time string value object.
"""

from datetime import time
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class StringTimeValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    Validate and normalize a string accepted by `datetime.time.fromisoformat`.

    Valid inputs are stored in the ISO 8601 representation produced by `datetime.time.isoformat`. For example,
    `14:30` becomes `14:30:00` and a `Z` UTC suffix becomes `+00:00`.

    Example:
    ```python
    from value_object_pattern.usables.dates import StringTimeValueObject

    meeting_time = StringTimeValueObject(value='14:30')
    print(repr(meeting_time))
    # >>> StringTimeValueObject(value='14:30:00')
    ```
    """

    _internal_time_object: time

    @process(order=0)
    def _normalize_time(self, value: str) -> str:
        """
        Normalize the parsed time to its ISO 8601 representation.

        Args:
            value (str): The validated time string.

        Returns:
            str: The normalized time string.
        """
        return self._internal_time_object.isoformat()

    @validation(order=1)
    def _ensure_value_is_time(self, value: str) -> None:
        """
        Parse and retain the time represented by the string.

        Args:
            value (str): The time string to validate.

        Raises:
            ValueError: If the value is not accepted by `datetime.time.fromisoformat`.
        """
        try:
            self._internal_time_object = time.fromisoformat(value)

        except ValueError:
            self._raise_value_is_not_valid_time(value=value)

    def _raise_value_is_not_valid_time(self, value: str) -> NoReturn:
        """
        Raise an error for an invalid time string.

        Args:
            value (str): The invalid time string.

        Raises:
            ValueError: Always raised with the invalid value.
        """
        raise ValueError(f'StringTimeValueObject value <<<{value}>>> is not a valid time.')
