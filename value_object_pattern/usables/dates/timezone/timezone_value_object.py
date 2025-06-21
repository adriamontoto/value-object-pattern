"""
TimezoneValueObject value object.
"""

from datetime import tzinfo
from typing import Any, NoReturn

from value_object_pattern.decorators import validation
from value_object_pattern.models import ValueObject


class TimezoneValueObject(ValueObject[tzinfo]):
    """
    TimezoneValueObject value object ensures the provided value is a timezone.

    Example:
    ```python
    from datetime import UTC

    from value_object_pattern.usables import TimezoneValueObject

    timezone = TimezoneValueObject(value=UTC)

    print(repr(timezone))
    # >>> TimezoneValueObject(value=UTC)
    ```
    """

    @validation(order=0)
    def _ensure_value_is_timezone(self, value: tzinfo) -> None:
        """
        Ensures the value object `value` is a timezone.

        Args:
            value (tzinfo): The provided value.

        Raises:
            TypeError: If the `value` is not a timezone.
        """
        if not isinstance(value, tzinfo):
            self._raise_value_is_not_timezone(value=value)

    def _raise_value_is_not_timezone(self, value: Any) -> NoReturn:
        """
        Raises a TypeError if the value object `value` is not a timezone.

        Args:
            value (Any): The provided value.

        Raises:
            TypeError: If the `value` is not a timezone.
        """
        raise TypeError(f'TimezoneValueObject value <<<{value}>>> must be a timezone. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip
