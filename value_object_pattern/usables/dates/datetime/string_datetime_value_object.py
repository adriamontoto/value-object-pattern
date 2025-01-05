"""
StringDatetimeValueObject value object.
"""

from __future__ import annotations

from datetime import UTC, datetime

from dateutil.parser import ParserError, parse
from dateutil.relativedelta import relativedelta

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .datetime_value_object import DatetimeValueObject


class StringDatetimeValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    StringDatetimeValueObject value object.
    """

    @process(order=0)
    def _ensure_value_is_normalized(self, value: str) -> str:
        """
        Ensures the value object value is normalized datetime string (ISO 8601, YYYY-MM-DDTHH:MM:SS).

        Args:
            value (str): Value.

        Returns:
            str: Value with the normalized datetime string.
        """
        return self._datetime_normalize(value=value).isoformat()

    @validation(order=0)
    def _ensure_value_is_date(self, value: str) -> None:
        """
        Ensures the value object value is a datetime.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not a datetime.
        """
        self._datetime_normalize(value=value)

    @classmethod
    def _datetime_normalize(cls, value: str) -> datetime:
        """
        Normalizes the given datetime.

        Args:
            value (str): datetime.

        Raises:
            TypeError: If the value is not a string.
            ValueError: If the value is not a valid datetime.

        Returns:
            str: Normalized datetime.
        """
        if type(value) is not str:
            raise TypeError(f'StringDatetimeValueObject value <<<{value}>>> must be a string. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip

        try:
            return parse(timestr=value)

        except ParserError as error:
            raise ValueError(f'StringDatetimeValueObject value <<<{value}>>> is not a valid datetime.') from error

    def is_today(self, *, reference_date: datetime | None = None) -> bool:
        """
        Determines whether the stored datetime value is today's datetime.

        Args:
            reference_date (datetime | None, optional): The datetime to compare against. If None, the current datetime
            (UTC) is used.

        Raises:
            TypeError: If the reference_date is not a datetime.

        Returns:
            bool: True if the stored datetime matches today's datetime, False otherwise.
        """
        return self.is_today_class(value=self.value, reference_date=reference_date)

    @classmethod
    def is_today_class(cls, *, value: str, reference_date: datetime | None = None) -> bool:
        """
        Determines whether a given datetime matches today's datetime.

        Args:
            value (str): The datetime to be checked.
            reference_date (datetime | None, optional): The datetime to compare against. If None, the current datetime
            (UTC) is used.

        Raises:
            TypeError: If the reference_date is not a datetime.

        Returns:
            bool: True if the given datetime matches today's datetime, False otherwise.
        """
        if reference_date is None:
            reference_date = datetime.now(tz=UTC)

        date_value = cls._datetime_normalize(value=value)
        DatetimeValueObject(value=reference_date)

        return date_value == reference_date

    def is_in_range(self, *, start_date: datetime, end_date: datetime) -> bool:
        """
        Determines whether the stored datetime value falls within the specified datetime range.

        Args:
            start_date (datetime): The beginning of the datetime range (inclusive).
            end_date (datetime): The end of the datetime range (inclusive).

        Raises:
            TypeError: If start_date is not a datetime.
            TypeError: If end_date is not a datetime.
            ValueError: If start_date is later than end_date.

        Returns:
            bool: True if the stored datetime is within the range, False otherwise.
        """
        return self.is_in_range_class(value=self.value, start_date=start_date, end_date=end_date)

    @classmethod
    def is_in_range_class(cls, *, value: str, start_date: datetime, end_date: datetime) -> bool:
        """
        Determines whether a given datetime falls within the specified datetime range.

        Args:
            value (str): The datetime to be checked.
            start_date (datetime): The beginning of the datetime range (inclusive).
            end_date (datetime): The end of the datetime range (inclusive).

        Raises:
            TypeError: If start_date is not a datetime.
            TypeError: If end_date is not a datetime.
            ValueError: If start_date is later than end_date.

        Returns:
            bool: True if the given datetime is within the range, False otherwise.
        """
        date_value = cls._datetime_normalize(value=value)
        DatetimeValueObject(value=start_date)
        DatetimeValueObject(value=end_date)

        if start_date > end_date:
            raise ValueError(f'StringDatetimeValueObject start_date <<<{start_date.isoformat()}>>> must be earlier than or equal to end_date <<<{end_date.isoformat()}>>>.')  # noqa: E501  # fmt: skip

        return start_date <= date_value <= end_date

    def calculate_age(self) -> int:
        """
        Calculates the age of the stored datetime value.

        Returns:
            int: The age in years of the stored datetime.
        """
        return self.calculate_age_class(value=self.value)

    @classmethod
    def calculate_age_class(cls, *, value: str) -> int:
        """
        Calculates the age of a given datetime.

        Args:
            value (str): The datetime to calculate the age of.

        Raises:
            TypeError: If the value is not a string.
            ValueError: If the value is not a valid datetime

        Returns:
            int: The age in years of the given datetime.
        """
        datetime_value = cls._datetime_normalize(value=value)

        return relativedelta(dt1=datetime.now(tz=UTC), dt2=datetime_value).years
