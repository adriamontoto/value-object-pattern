"""
Provide a strictly negative duration value object.
"""

from datetime import timedelta
from typing import NoReturn

from value_object_pattern.decorators import validation

from .duration_value_object import DurationValueObject


class NegativeDurationValueObject(DurationValueObject):
    """
    Validate and store an exact, strictly negative `datetime.timedelta` value.

    Example:
    ```python
    from datetime import timedelta

    from value_object_pattern.usables.dates import NegativeDurationValueObject

    offset = NegativeDurationValueObject(value=timedelta(seconds=-30))
    print(repr(offset))
    # >>> NegativeDurationValueObject(value=datetime.timedelta(days=-1, seconds=86370))
    ```
    """

    @validation(order=1)
    def _ensure_value_is_negative(self, value: timedelta) -> None:
        """
        Ensure the duration is less than zero.

        Args:
            value (timedelta): The provided duration.

        Raises:
            ValueError: If the duration is zero or positive.
        """
        if value >= timedelta():
            self._raise_value_is_not_negative(value=value)

    def _raise_value_is_not_negative(self, value: timedelta) -> NoReturn:
        """
        Raise an error for a duration that is not negative.

        Args:
            value (timedelta): The invalid duration.

        Raises:
            ValueError: Always raised with the invalid value.
        """
        raise ValueError(f'DurationValueObject value <<<{value}>>> must be a negative duration.')
