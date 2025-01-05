"""
DateValueObject value object.
"""

from __future__ import annotations

from datetime import UTC, date, datetime

from dateutil.relativedelta import relativedelta

from value_object_pattern.decorators import validation
from value_object_pattern.models import ValueObject


class DateValueObject(ValueObject[date]):
    """
    DateValueObject value object.
    """

    @validation(order=0)
    def _ensure_value_is_date(self, value: date) -> None:
        """
        Ensures the value object value is a date.

        Args:
            value (date): Value.

        Raises:
            TypeError: If the value is not a date.
        """
        if type(value) is not date:
            raise TypeError(f'DateValueObject value <<<{value}>>> must be a date. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip

    def is_today(self, *, reference_date: date | None = None) -> bool:
        """
        Determines whether the stored date value is today's date.

        Args:
            reference_date (date | None, optional): The date to compare against. If None, the current date (UTC) is
            used.

        Raises:
            TypeError: If the value is not a date.
            TypeError: If the reference_date is not a date.

        Returns:
            bool: True if the stored date matches today's date, False otherwise.
        """
        return self.is_today_class(value=self.value, reference_date=reference_date)

    @classmethod
    def is_today_class(cls, *, value: date, reference_date: date | None = None) -> bool:
        """
        Determines whether a given date matches today's date.

        Args:
            value (date): The date to be checked.
            reference_date (date | None, optional): The date to compare against. If None, the current date (UTC) is
            used.

        Raises:
            TypeError: If the value is not a date.
            TypeError: If the reference_date is not a date.

        Returns:
            bool: True if the given date matches today's date, False otherwise.
        """
        if reference_date is None:
            reference_date = datetime.now(tz=UTC).date()

        DateValueObject(value=value)
        DateValueObject(value=reference_date)

        return value == reference_date

    def is_in_range(self, *, start_date: date, end_date: date) -> bool:
        """
        Determines whether the stored date value falls within the specified date range.

        Args:
            start_date (date): The beginning of the date range (inclusive).
            end_date (date): The end of the date range (inclusive).

        Raises:
            TypeError: If the value is not a date.
            TypeError: If start_date is not a date.
            TypeError: If end_date is not a date.
            ValueError: If start_date is later than end_date.

        Returns:
            bool: True if the stored date is within the range, False otherwise.
        """
        return self.is_in_range_class(value=self.value, start_date=start_date, end_date=end_date)

    @classmethod
    def is_in_range_class(cls, *, value: date, start_date: date, end_date: date) -> bool:
        """
        Determines whether a given date falls within the specified date range.

        Args:
            value (date): The date to be checked.
            start_date (date): The beginning of the date range (inclusive).
            end_date (date): The end of the date range (inclusive).

        Raises:
            TypeError: If the value is not a date.
            TypeError: If start_date is not a date.
            TypeError: If end_date is not a date.
            ValueError: If start_date is later than end_date.

        Returns:
            bool: True if the given date is within the range, False otherwise.
        """
        DateValueObject(value=value)
        DateValueObject(value=start_date)
        DateValueObject(value=end_date)

        if start_date > end_date:
            raise ValueError(f'DateValueObject start_date <<<{start_date.isoformat()}>>> must be earlier than or equal to end_date <<<{end_date.isoformat()}>>>.')  # noqa: E501  # fmt: skip

        return start_date <= value <= end_date

    def calculate_age(self) -> int:
        """
        Calculates the age of the stored date value.

        Returns:
            int: The age in years of the stored date.
        """
        return self.calculate_age_class(value=self.value)

    @classmethod
    def calculate_age_class(cls, *, value: date) -> int:
        """
        Calculates the age of a given date.

        Args:
            value (date): The date to calculate the age of.

        Raises:
            TypeError: If the value is not a date.

        Returns:
            int: The age in years of the given date.
        """
        DateValueObject(value=value)

        return relativedelta(dt1=datetime.now(tz=UTC).date(), dt2=value).years
