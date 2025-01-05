"""
DatetimeValueObject value object.
"""

from __future__ import annotations

from datetime import UTC, datetime

from dateutil.relativedelta import relativedelta

from value_object_pattern.decorators import validation
from value_object_pattern.models import ValueObject


class DatetimeValueObject(ValueObject[datetime]):
    """
    DatetimeValueObject value object.
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
            TypeError: If the value is not a datetime.
            TypeError: If the reference_datetime is not a datetime.

        Returns:
            bool: True if the stored datetime matches the current datetime, False otherwise.
        """
        return self.is_now_class(value=self.value, reference_datetime=reference_datetime)

    @classmethod
    def is_now_class(cls, *, value: datetime, reference_datetime: datetime | None = None) -> bool:
        """
        Determines whether a given datetime matches the current datetime.

        Args:
            value (datetime): The datetime to be checked.
            reference_datetime (datetime | None, optional): The datetime to compare against. If None, the current
            datetime (UTC) is used.

        Raises:
            TypeError: If the value is not a datetime.
            TypeError: If the reference_datetime is not a datetime.

        Returns:
            bool: True if the given datetime matches the current datetime, False otherwise.
        """
        if reference_datetime is None:
            reference_datetime = datetime.now(tz=UTC)

        DatetimeValueObject(value=value)
        DatetimeValueObject(value=reference_datetime)

        return value == reference_datetime

    def is_in_range(self, *, start_datetime: datetime, end_datetime: datetime) -> bool:
        """
        Determines whether the stored datetime value falls within the specified datetime range.

        Args:
            start_datetime (datetime): The beginning of the datetime range (inclusive).
            end_datetime (datetime): The end of the datetime range (inclusive).

        Raises:
            TypeError: If the value is not a datetime.
            TypeError: If start_datetime is not a datetime.
            TypeError: If end_datetime is not a datetime.
            ValueError: If start_datetime is later than end_datetime.

        Returns:
            bool: True if the stored datetime is within the range, False otherwise.
        """
        return self.is_in_range_class(value=self.value, start_datetime=start_datetime, end_datetime=end_datetime)

    @classmethod
    def is_in_range_class(cls, *, value: datetime, start_datetime: datetime, end_datetime: datetime) -> bool:
        """
        Determines whether a given datetime falls within the specified datetime range.

        Args:
            value (datetime): The datetime to be checked.
            start_datetime (datetime): The beginning of the datetime range (inclusive).
            end_datetime (datetime): The end of the datetime range (inclusive).

        Raises:
            TypeError: If the value is not a datetime.
            TypeError: If start_datetime is not a datetime.
            TypeError: If end_datetime is not a datetime.
            ValueError: If start_datetime is later than end_datetime.

        Returns:
            bool: True if the given datetime is within the range, False otherwise.
        """
        DatetimeValueObject(value=value)
        DatetimeValueObject(value=start_datetime)
        DatetimeValueObject(value=end_datetime)

        if start_datetime > end_datetime:
            raise ValueError(f'DatetimeValueObject start_datetime <<<{start_datetime.isoformat()}>>> must be earlier than or equal to end_datetime <<<{end_datetime.isoformat()}>>>.')  # noqa: E501  # fmt: skip

        return start_datetime <= value <= end_datetime

    def calculate_age(self) -> int:
        """
        Calculates the age of the stored datetime value.

        Returns:
            int: The age in years of the stored datetime.
        """
        return self.calculate_age_class(value=self.value)

    @classmethod
    def calculate_age_class(cls, *, value: datetime) -> int:
        """
        Calculates the age of a given datetime.

        Args:
            value (datetime): The datetime to calculate the age of.

        Raises:
            TypeError: If the value is not a datetime.

        Returns:
            int: The age in years of the given datetime.
        """
        DatetimeValueObject(value=value)

        return relativedelta(dt1=datetime.now(tz=UTC), dt2=value).years
