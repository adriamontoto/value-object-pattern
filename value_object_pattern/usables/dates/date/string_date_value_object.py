"""
StringDateValueObject value object.
"""

from __future__ import annotations

from datetime import UTC, date, datetime

from dateutil.parser import ParserError, parse
from dateutil.relativedelta import relativedelta

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .date_value_object import DateValueObject


class StringDateValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    StringDateValueObject value object.
    """

    @process(order=0)
    def _ensure_value_is_normalized(self, value: str) -> str:
        """
        Ensures the value object value is normalized date string (ISO 8601, YYYY-MM-DD).

        Args:
            value (str): Value.

        Returns:
            str: Value with the normalized date string.
        """
        return self._date_normalize(value=value).isoformat()

    @validation(order=0)
    def _ensure_value_is_date(self, value: str) -> None:
        """
        Ensures the value object value is a date.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not a date.
        """
        self._date_normalize(value=value)

    @classmethod
    def _date_normalize(cls, value: str) -> date:
        """
        Normalizes the given date.

        Args:
            value (str): Date.

        Raises:
            TypeError: If the value is not a string.
            ValueError: If the value is not a valid date.

        Returns:
            str: Normalized date.
        """
        if type(value) is not str:
            raise TypeError(f'StringDateValueObject value <<<{value}>>> must be a string. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip

        try:
            return parse(timestr=value).date()

        except ParserError as error:
            raise ValueError(f'StringDateValueObject value <<<{value}>>> is not a valid date.') from error

    def is_today(self, *, reference_date: date | None = None) -> bool:
        """
        Determines whether the stored date value is today's date.

        Args:
            reference_date (date | None, optional): The date to compare against. If None, the current date (UTC) is
            used.

        Raises:
            TypeError: If the reference_date is not a date.

        Returns:
            bool: True if the stored date matches today's date, False otherwise.
        """
        return self.is_today_class(value=self.value, reference_date=reference_date)

    @classmethod
    def is_today_class(cls, *, value: str, reference_date: date | None = None) -> bool:
        """
        Determines whether a given date matches today's date.

        Args:
            value (str): The date to be checked.
            reference_date (date | None, optional): The date to compare against. If None, the current date (UTC) is
            used.

        Raises:
            TypeError: If the reference_date is not a date.

        Returns:
            bool: True if the given date matches today's date, False otherwise.
        """
        if reference_date is None:
            reference_date = datetime.now(tz=UTC).date()

        date_value = cls._date_normalize(value=value)
        DateValueObject(value=reference_date)

        return date_value == reference_date

    def is_in_range(self, *, start_date: date, end_date: date) -> bool:
        """
        Determines whether the stored date value falls within the specified date range.

        Args:
            start_date (date): The beginning of the date range (inclusive).
            end_date (date): The end of the date range (inclusive).

        Raises:
            TypeError: If start_date is not a date.
            TypeError: If end_date is not a date.
            ValueError: If start_date is later than end_date.

        Returns:
            bool: True if the stored date is within the range, False otherwise.
        """
        return self.is_in_range_class(value=self.value, start_date=start_date, end_date=end_date)

    @classmethod
    def is_in_range_class(cls, *, value: str, start_date: date, end_date: date) -> bool:
        """
        Determines whether a given date falls within the specified date range.

        Args:
            value (str): The date to be checked.
            start_date (date): The beginning of the date range (inclusive).
            end_date (date): The end of the date range (inclusive).

        Raises:
            TypeError: If start_date is not a date.
            TypeError: If end_date is not a date.
            ValueError: If start_date is later than end_date.

        Returns:
            bool: True if the given date is within the range, False otherwise.
        """
        date_value = cls._date_normalize(value=value)
        DateValueObject(value=start_date)
        DateValueObject(value=end_date)

        if start_date > end_date:
            raise ValueError(f'StringDateValueObject start_date <<<{start_date.isoformat()}>>> must be earlier than or equal to end_date <<<{end_date.isoformat()}>>>.')  # noqa: E501  # fmt: skip

        return start_date <= date_value <= end_date

    def calculate_age(self) -> int:
        """
        Calculates the age of the stored date value.

        Returns:
            int: The age in years of the stored date.
        """
        return self.calculate_age_class(value=self.value)

    @classmethod
    def calculate_age_class(cls, *, value: str) -> int:
        """
        Calculates the age of a given date.

        Args:
            value (str): The date to calculate the age of.

        Raises:
            TypeError: If the value is not a string.
            ValueError: If the value is not a valid date

        Returns:
            int: The age in years of the given date.
        """
        date_value = cls._date_normalize(value=value)

        return relativedelta(dt1=datetime.now(tz=UTC).date(), dt2=date_value).years
