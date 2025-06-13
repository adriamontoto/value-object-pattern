"""
StringDateValueObject value object.
"""

from datetime import UTC, date, datetime

from dateutil.parser import ParserError, parse
from dateutil.relativedelta import relativedelta

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .date_value_object import DateValueObject


class StringDateValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    StringDateValueObject value object ensures the provided value is a valid date.

    Example:
    ```python
    from value_object_pattern.usables.dates import StringDateValueObject

    now = '1900-01-01'
    date = StringDateValueObject(value=now)

    print(repr(date))
    # >>> StringDateValueObject(value=1900-01-01)
    ```
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

        Example:
        ```python
        from datetime import date

        from value_object_pattern.usables.dates import StringDateValueObject

        now = '1900-01-01'
        today = date(year=1900, month=1, day=1)
        is_today = StringDateValueObject(value=now).is_today(reference_date=today)

        print(is_today)
        # >>> True
        ```
        """
        if reference_date is None:
            reference_date = datetime.now(tz=UTC).date()

        date_value = self._date_normalize(value=self.value)
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

        Example:
        ```python
        from datetime import date

        from value_object_pattern.usables.dates import StringDateValueObject

        now = '1900-01-01'
        start_date = date(year=1899, month=12, day=31)
        end_date = date(year=1900, month=1, day=2)
        is_in_range = StringDateValueObject(
            value=now,
        ).is_in_range(
            start_date=start_date,
            end_date=end_date,
        )

        print(is_in_range)
        # >>> True
        ```
        """
        date_value = self._date_normalize(value=self.value)
        DateValueObject(value=start_date)
        DateValueObject(value=end_date)

        if start_date > end_date:
            raise ValueError(f'StringDateValueObject start_date <<<{start_date.isoformat()}>>> must be earlier than or equal to end_date <<<{end_date.isoformat()}>>>.')  # noqa: E501  # fmt: skip

        return start_date <= date_value <= end_date

    def calculate_age(self, *, reference_date: date | None = None) -> int:
        """
        Calculates the age of the stored date value.

        Args:
            reference_date (date | None, optional): The date to calculate the age from. If None, the current date (UTC)
            is used.

        Raises:
            TypeError: If the reference_date is not a date.
            ValueError: If the stored date is later than the reference_date.

        Returns:
            int: The age in years of the stored date.

        Example:
        ```python
        from datetime import date

        from value_object_pattern.usables.dates import StringDateValueObject

        now = '1900-01-01'
        today = date(year=2000, month=1, day=1)
        age = StringDateValueObject(value=now).calculate_age(reference_date=today)

        print(age)
        # >>> 100
        ```
        """
        if reference_date is None:
            reference_date = datetime.now(tz=UTC).date()

        date_value = self._date_normalize(value=self.value)
        DateValueObject(value=reference_date)

        if date_value > reference_date:
            raise ValueError(f'StringDateValueObject value <<<{date_value.isoformat()}>>> must be earlier than or equal to reference_date <<<{reference_date.isoformat()}>>>.')  # noqa: E501  # fmt: skip

        return relativedelta(dt1=reference_date, dt2=date_value).years
