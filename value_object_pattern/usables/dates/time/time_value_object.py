"""
Provide a datetime.time value object.
"""

from datetime import time
from typing import Any, NoReturn

from value_object_pattern import ValueObject
from value_object_pattern.decorators import validation


class TimeValueObject(ValueObject[time]):
    """
    Validate and store an exact `datetime.time` value.

    Example:
    ```python
    from datetime import time

    from value_object_pattern.usables.dates import TimeValueObject

    meeting_time = TimeValueObject(value=time(hour=14, minute=30))
    print(repr(meeting_time))
    # >>> TimeValueObject(value=datetime.time(14, 30))
    ```
    """

    @validation(order=0)
    def _ensure_value_is_time(self, value: time) -> None:
        """
        Ensure the value is exactly a datetime.time.

        Args:
            value (time): The value to validate.

        Raises:
            TypeError: If the value is not exactly a datetime.time.
        """
        if type(value) is not time:
            self._raise_value_is_not_time(value=value)

    def _raise_value_is_not_time(self, value: Any) -> NoReturn:
        """
        Raise an error for a non-time value.

        Args:
            value (Any): The invalid value.

        Raises:
            TypeError: Always raised with the invalid type.
        """
        raise TypeError(f'TimeValueObject value <<<{value}>>> must be a time. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip
