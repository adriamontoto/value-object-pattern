"""
DatetimeValueObject value object.
"""

from datetime import datetime
from typing import Any, NoReturn

from dateutil.relativedelta import relativedelta

from value_object_pattern.decorators import validation
from value_object_pattern.models import ValueObject


class DatetimeValueObject(ValueObject[datetime]):
    """
    DatetimeValueObject value object ensures the provided value is a datetime.

    Example:
    ```python
    from datetime import UTC, datetime

    from value_object_pattern.usables.dates import DatetimeValueObject

    now = datetime(year=1900, month=1, day=1, hour=0, minute=0, second=0, tzinfo=UTC)
    date_ = DatetimeValueObject(value=now)

    print(repr(date_))
    # >>> DatetimeValueObject(value=datetime.datetime(1900, 1, 1, 0, 0, tzinfo=datetime.timezone.utc))
    ```
    """

    @validation(order=0)
    def _ensure_value_is_datetime(self, value: datetime) -> None:
        """
        Ensures the value object value is a datetime.

        Args:
            value (datetime): Value.

        Raises:
            TypeError: If the value is not a datetime.
        """
        if type(value) is not datetime:
            self._raise_value_is_not_datetime(value=value)

    def _raise_value_is_not_datetime(self, value: Any) -> NoReturn:
        """
        Raises a TypeError if the value object `value` is not a datetime.

        Args:
            value (Any): The provided value.

        Raises:
            TypeError: If the `value` is not a datetime.
        """
        raise TypeError(f'DatetimeValueObject value <<<{value}>>> must be a datetime. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip

    def is_now(self, *, reference_datetime: datetime) -> bool:
        """
        Determines whether the stored datetime value matches the current datetime.

        Args:
            reference_datetime (datetime): The datetime to compare against.

        Raises:
            TypeError: If the `reference_datetime` is not a datetime.

        Returns:
            bool: True if the stored datetime matches the current datetime, False otherwise.

        Example:
        ```python
        from datetime import UTC, datetime

        from value_object_pattern.usables.dates import DatetimeValueObject

        now = datetime(year=1900, month=1, day=1, hour=8, minute=30, second=0, tzinfo=UTC)
        today = datetime(year=1900, month=1, day=1, hour=0, minute=0, second=0, tzinfo=UTC)
        is_now = DatetimeValueObject(value=now).is_now(reference_datetime=today)

        print(is_now)
        # >>> False
        ```
        """
        DatetimeValueObject(value=reference_datetime, parameter='reference_datetime')

        return self.value == reference_datetime

    def is_today(self, *, reference_datetime: datetime) -> bool:
        """
        Determines whether the stored datetime value is today's datetime.

        Args:
            reference_datetime (datetime): The datetime to compare against.

        Raises:
            TypeError: If the `reference_datetime` is not a datetime.

        Returns:
            bool: True if the stored datetime matches today's datetime, False otherwise.

        Example:
        ```python
        from datetime import UTC, datetime

        from value_object_pattern.usables.dates import DatetimeValueObject

        now = datetime(year=1900, month=1, day=1, hour=8, minute=30, second=0, tzinfo=UTC)
        today = datetime(year=1900, month=1, day=1, hour=0, minute=0, second=0, tzinfo=UTC)
        is_today = DatetimeValueObject(value=now).is_today(reference_datetime=today)

        print(is_today)
        # >>> True
        ```
        """
        DatetimeValueObject(value=reference_datetime, parameter='reference_datetime')

        return self.value.date() == reference_datetime.date()

    def is_later_than(self, *, reference_datetime: datetime) -> bool:
        """
        Determines whether the stored datetime value is later than the specified datetime (same day not included).

        Args:
            reference_datetime (datetime): The datetime to compare against.

        Raises:
            TypeError: If the `reference_datetime` is not a datetime.

        Returns:
            bool: True if the stored datetime is later than the `reference_datetime`, False otherwise.

        Example:
        ```python
        from datetime import UTC, datetime

        from value_object_pattern.usables.dates import DatetimeValueObject

        now = datetime(year=1900, month=1, day=1, hour=8, minute=30, second=0, tzinfo=UTC)
        reference_datetime = datetime(year=1899, month=12, day=31, hour=23, minute=59, second=59, tzinfo=UTC)
        is_later_than = DatetimeValueObject(value=now).is_later_than(reference_datetime=reference_datetime)

        print(is_later_than)
        # >>> True
        ```
        """
        DatetimeValueObject(value=reference_datetime, parameter='reference_datetime')

        return self.value > reference_datetime

    def is_in_range(self, *, start_datetime: datetime, end_datetime: datetime) -> bool:
        """
        Determines whether the stored datetime value falls within the specified datetime range (both inclusive).

        Args:
            start_datetime (datetime): The beginning of the datetime range.
            end_datetime (datetime): The end of the datetime range.

        Raises:
            TypeError: If the `start_datetime` is not a datetime.
            TypeError: If the `end_datetime` is not a datetime.
            ValueError: If the `start_datetime` is later than the `end_datetime`.

        Returns:
            bool: True if the stored datetime is within the range, False otherwise.

        Example:
        ```python
        from datetime import UTC, datetime

        from value_object_pattern.usables.dates import DatetimeValueObject

        now = datetime(year=1900, month=1, day=1, hour=0, minute=0, second=0, tzinfo=UTC)
        start_datetime = datetime(year=1899, month=12, day=31, hour=23, minute=59, second=59, tzinfo=UTC)
        end_datetime = datetime(year=1900, month=1, day=2, hour=00, minute=00, second=00, tzinfo=UTC)
        is_in_range = DatetimeValueObject(
            value=now,
        ).is_in_range(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )

        print(is_in_range)
        # >>> True
        ```
        """
        DatetimeValueObject(value=start_datetime, parameter='start_datetime')
        DatetimeValueObject(value=end_datetime, parameter='end_datetime')

        if start_datetime > end_datetime:
            raise self._raise_start_datetime_is_later_than_end_datetime(start_datetime=start_datetime, end_datetime=end_datetime)  # noqa: E501  # fmt: skip

        return start_datetime <= self.value <= end_datetime

    def _raise_start_datetime_is_later_than_end_datetime(
        self,
        *,
        start_datetime: datetime,
        end_datetime: datetime,
    ) -> NoReturn:
        """
        Raises a ValueError if the start datetime is later than the end datetime.

        Args:
            start_datetime (datetime): The start datetime.
            end_datetime (datetime): The end datetime.

        Raises:
            ValueError: If the `start_datetime` is later than the `end_datetime`.
        """
        raise ValueError(f'DatetimeValueObject start_datetime <<<{start_datetime.isoformat()}>>> must be earlier than or equal to end_datetime <<<{end_datetime.isoformat()}>>>.')  # noqa: E501  # fmt: skip

    def calculate_age(self, *, reference_datetime: datetime) -> int:
        """
        Calculates the age of a given datetime.

        Args:
            reference_datetime (datetime): The datetime to calculate the age against.

        Raises:
            TypeError: If the `reference_datetime` is not a datetime.
            ValueError: If the stored datetime is later than the `reference_datetime`.

        Returns:
            int: The age in years of the given datetime.

        Example:
        ```python
        from datetime import UTC, datetime

        from value_object_pattern.usables.dates import DatetimeValueObject

        now = datetime(year=1900, month=1, day=1, hour=0, minute=0, second=0, tzinfo=UTC)
        today = datetime(year=2000, month=1, day=1, hour=0, minute=0, second=0, tzinfo=UTC)
        age = DatetimeValueObject(value=now).calculate_age(reference_datetime=today)

        print(age)
        # >>> 100
        ```
        """
        DatetimeValueObject(value=reference_datetime, parameter='reference_datetime')

        if self.value > reference_datetime:
            self._raise_start_datetime_is_later_than_end_datetime(start_datetime=self.value, end_datetime=reference_datetime)  # noqa: E501  # fmt: skip

        return relativedelta(dt1=reference_datetime, dt2=self.value).years
