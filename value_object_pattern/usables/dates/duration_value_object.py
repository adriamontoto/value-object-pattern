"""
Provide a non-negative duration value object.
"""

from datetime import timedelta
from typing import Any, NoReturn, Self

from value_object_pattern.decorators import validation
from value_object_pattern.models import ValueObject
from value_object_pattern.usables import PositiveOrZeroIntegerValueObject


class DurationValueObject(ValueObject[timedelta]):
    """
    Validate and store an exact, non-negative `datetime.timedelta` value.

    Zero is a valid duration. Negative timedeltas are rejected. Named constructors accept whole units and conversion
    methods return the complete duration in the requested unit, including days instead of only the remainder exposed by
    `timedelta.seconds`.

    Example:
    ```python
    from datetime import timedelta

    from value_object_pattern.usables.dates import DurationValueObject

    timeout = DurationValueObject(value=timedelta(seconds=30))
    print(repr(timeout))
    # >>> DurationValueObject(value=datetime.timedelta(seconds=30))
    ```
    """

    @classmethod
    def from_seconds(cls, *, seconds: int, title: str | None = None, parameter: str | None = None) -> Self:
        """
        Create a duration from a whole number of seconds.

        Args:
            seconds (int): The number of seconds.
            title (str | None, optional): Title used in validation errors. Defaults to None.
            parameter (str | None, optional): Parameter used in validation errors. Defaults to None.

        Raises:
            TypeError: If `seconds` is not an integer.
            ValueError: If `seconds` is negative.

        Returns:
            Self: A duration containing the requested number of seconds.

        Example:
        ```python
        from value_object_pattern.usables.dates import DurationValueObject

        timeout = DurationValueObject.from_seconds(seconds=30)
        print(repr(timeout.value))
        # >>> datetime.timedelta(seconds=30)
        ```
        """
        PositiveOrZeroIntegerValueObject(value=seconds, title='DurationValueObject', parameter='seconds')

        return cls(value=timedelta(seconds=seconds), title=title, parameter=parameter)

    @classmethod
    def from_minutes(cls, *, minutes: int, title: str | None = None, parameter: str | None = None) -> Self:
        """
        Create a duration from a whole number of minutes.

        Args:
            minutes (int): The number of minutes.
            title (str | None, optional): Title used in validation errors. Defaults to None.
            parameter (str | None, optional): Parameter used in validation errors. Defaults to None.

        Raises:
            TypeError: If `minutes` is not an integer.
            ValueError: If `minutes` is negative.

        Returns:
            Self: A duration containing the requested number of minutes.

        Example:
        ```python
        from value_object_pattern.usables.dates import DurationValueObject

        timeout = DurationValueObject.from_minutes(minutes=5)
        print(repr(timeout.value))
        # >>> datetime.timedelta(seconds=300)
        ```
        """
        PositiveOrZeroIntegerValueObject(value=minutes, title='DurationValueObject', parameter='minutes')

        return cls(value=timedelta(minutes=minutes), title=title, parameter=parameter)

    @classmethod
    def from_hours(cls, *, hours: int, title: str | None = None, parameter: str | None = None) -> Self:
        """
        Create a duration from a whole number of hours.

        Args:
            hours (int): The number of hours.
            title (str | None, optional): Title used in validation errors. Defaults to None.
            parameter (str | None, optional): Parameter used in validation errors. Defaults to None.

        Raises:
            TypeError: If `hours` is not an integer.
            ValueError: If `hours` is negative.

        Returns:
            Self: A duration containing the requested number of hours.

        Example:
        ```python
        from value_object_pattern.usables.dates import DurationValueObject

        timeout = DurationValueObject.from_hours(hours=2)
        print(repr(timeout.value))
        # >>> datetime.timedelta(seconds=7200)
        ```
        """
        PositiveOrZeroIntegerValueObject(value=hours, title='DurationValueObject', parameter='hours')

        return cls(value=timedelta(hours=hours), title=title, parameter=parameter)

    @classmethod
    def from_days(cls, *, days: int, title: str | None = None, parameter: str | None = None) -> Self:
        """
        Create a duration from a whole number of days.

        Args:
            days (int): The number of days.
            title (str | None, optional): Title used in validation errors. Defaults to None.
            parameter (str | None, optional): Parameter used in validation errors. Defaults to None.

        Raises:
            TypeError: If `days` is not an integer.
            ValueError: If `days` is negative.

        Returns:
            Self: A duration containing the requested number of days.

        Example:
        ```python
        from value_object_pattern.usables.dates import DurationValueObject

        timeout = DurationValueObject.from_days(days=1)
        print(repr(timeout.value))
        # >>> datetime.timedelta(days=1)
        ```
        """
        PositiveOrZeroIntegerValueObject(value=days, title='DurationValueObject', parameter='days')

        return cls(value=timedelta(days=days), title=title, parameter=parameter)

    def to_seconds(self) -> float:
        """
        Return the complete duration in seconds.

        Returns:
            float: Total elapsed seconds, including fractional microseconds and full days.

        Example:
        ```python
        from value_object_pattern.usables.dates import DurationValueObject

        duration = DurationValueObject.from_minutes(minutes=5)
        print(duration.to_seconds())
        # >>> 300.0
        ```
        """
        return self.value.total_seconds()

    def to_minutes(self) -> float:
        """
        Return the complete duration in minutes.

        Returns:
            float: Total elapsed minutes, including fractional seconds and full days.

        Example:
        ```python
        from value_object_pattern.usables.dates import DurationValueObject

        duration = DurationValueObject.from_seconds(seconds=90)
        print(duration.to_minutes())
        # >>> 1.5
        ```
        """
        return self.to_seconds() / 60

    def to_hours(self) -> float:
        """
        Return the complete duration in hours.

        Returns:
            float: Total elapsed hours, including fractional minutes and full days.

        Example:
        ```python
        from value_object_pattern.usables.dates import DurationValueObject

        duration = DurationValueObject.from_minutes(minutes=90)
        print(duration.to_hours())
        # >>> 1.5
        ```
        """
        return self.to_seconds() / 3_600

    def to_days(self) -> float:
        """
        Return the complete duration in days.

        Returns:
            float: Total elapsed days, including fractional hours.

        Example:
        ```python
        from value_object_pattern.usables.dates import DurationValueObject

        duration = DurationValueObject.from_hours(hours=36)
        print(duration.to_days())
        # >>> 1.5
        ```
        """
        return self.to_seconds() / 86_400

    @validation(order=0)
    def _ensure_value_is_timedelta(self, value: timedelta) -> None:
        """
        Ensure the value is exactly a datetime.timedelta.

        Args:
            value (timedelta): The value to validate.

        Raises:
            TypeError: If the value is not exactly a datetime.timedelta.
        """
        if type(value) is not timedelta:
            self._raise_value_is_not_timedelta(value=value)

    def _raise_value_is_not_timedelta(self, value: Any) -> NoReturn:
        """
        Raise an error for a non-timedelta value.

        Args:
            value (Any): The invalid value.

        Raises:
            TypeError: Always raised with the invalid type.
        """
        raise TypeError(f'DurationValueObject value <<<{value}>>> must be a timedelta. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip

    @validation(order=1)
    def _ensure_value_is_non_negative(self, value: timedelta) -> None:
        """
        Ensure the duration is zero or greater.

        Args:
            value (timedelta): The duration to validate.

        Raises:
            ValueError: If the duration is negative.
        """
        if value < timedelta():
            self._raise_value_is_negative(value=value)

    def _raise_value_is_negative(self, value: timedelta) -> NoReturn:
        """
        Raise an error for a negative duration.

        Args:
            value (timedelta): The negative duration.

        Raises:
            ValueError: Always raised with the invalid value.
        """
        raise ValueError(f'DurationValueObject value <<<{value}>>> must be non-negative.')
