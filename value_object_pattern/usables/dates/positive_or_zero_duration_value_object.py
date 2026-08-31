"""
Provide a positive-or-zero duration value object.
"""

from datetime import timedelta
from typing import NoReturn

from value_object_pattern.decorators import validation

from .duration_value_object import DurationValueObject


class PositiveOrZeroDurationValueObject(DurationValueObject):
    """
    Validate and store an exact, positive-or-zero `datetime.timedelta` value.

    Example:
    ```python
    from datetime import timedelta

    from value_object_pattern.usables.dates import PositiveOrZeroDurationValueObject

    timeout = PositiveOrZeroDurationValueObject(value=timedelta())
    print(repr(timeout))
    # >>> PositiveOrZeroDurationValueObject(value=datetime.timedelta(0))
    ```
    """

    @validation(order=1)
    def _ensure_value_is_positive_or_zero(self, value: timedelta) -> None:
        """
        Ensure the duration is greater than or equal to zero.

        Args:
            value (timedelta): The provided duration.

        Raises:
            ValueError: If the duration is negative.
        """
        if value < timedelta():
            self._raise_value_is_not_positive_or_zero(value=value)

    def _raise_value_is_not_positive_or_zero(self, value: timedelta) -> NoReturn:
        """
        Raise an error for a duration that is not positive or zero.

        Args:
            value (timedelta): The invalid duration.

        Raises:
            ValueError: Always raised with the invalid value.
        """
        raise ValueError(f'DurationValueObject value <<<{value}>>> must be a positive or zero duration.')
