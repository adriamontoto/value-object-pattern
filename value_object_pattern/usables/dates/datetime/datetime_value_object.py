"""
DatetimeValueObject value object.
"""

from datetime import UTC, datetime

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
    date = DatetimeValueObject(value=now)

    print(repr(date))
    # >>> DatetimeValueObject(value=1900-01-01T00:00:00+00:00)
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
            raise TypeError(f'DatetimeValueObject value <<<{value}>>> must be a datetime. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip

    def is_now(self, *, reference_datetime: datetime | None = None) -> bool:
        """
        Determines whether the stored datetime value matches the current datetime.

        Args:
            reference_datetime (datetime | None, optional): The datetime to compare against. If None, the current
            datetime (UTC) is used.

        Raises:
            TypeError: If the reference_datetime is not a datetime.

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
        if reference_datetime is None:
            reference_datetime = datetime.now(tz=UTC)

        DatetimeValueObject(value=reference_datetime)

        return self.value == reference_datetime

    def is_today(self, *, reference_datetime: datetime | None = None) -> bool:
        """
        Determines whether the stored datetime value is today's datetime.

        Args:
            reference_datetime (datetime | None, optional): The datetime to compare against. If None, the current
            datetime (UTC) is used.

        Raises:
            TypeError: If the reference_datetime is not a datetime.

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
        if reference_datetime is None:
            reference_datetime = datetime.now(tz=UTC)

        DatetimeValueObject(value=reference_datetime)

        return self.value.date() == reference_datetime.date()

    def is_in_range(self, *, start_datetime: datetime, end_datetime: datetime) -> bool:
        """
        Determines whether the stored datetime value falls within the specified datetime range.

        Args:
            start_datetime (datetime): The beginning of the datetime range (inclusive).
            end_datetime (datetime): The end of the datetime range (inclusive).

        Raises:
            TypeError: If start_datetime is not a datetime.
            TypeError: If end_datetime is not a datetime.
            ValueError: If start_datetime is later than end_datetime.

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
        DatetimeValueObject(value=start_datetime)
        DatetimeValueObject(value=end_datetime)

        if start_datetime > end_datetime:
            raise ValueError(f'DatetimeValueObject start_datetime <<<{start_datetime.isoformat()}>>> must be earlier than or equal to end_datetime <<<{end_datetime.isoformat()}>>>.')  # noqa: E501  # fmt: skip

        return start_datetime <= self.value <= end_datetime

    def calculate_age(self, *, reference_datetime: datetime | None = None) -> int:
        """
        Calculates the age of a given datetime.

        Args:
            reference_datetime (datetime | None, optional): The datetime to calculate the age against. If None, the
            current datetime (UTC) is used.

        Raises:
            TypeError: If the reference_datetime is not a datetime.
            ValueError: If the stored datetime is later than the reference_datetime.

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
        if reference_datetime is None:
            reference_datetime = datetime.now(tz=UTC)

        DatetimeValueObject(value=reference_datetime)

        return relativedelta(dt1=reference_datetime, dt2=self.value).years
