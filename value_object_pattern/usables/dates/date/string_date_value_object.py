"""
StringDateValueObject value object.
"""

from datetime import date
from typing import NoReturn

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
    # >>> StringDateValueObject(value='1900-01-01')
    ```
    """

    _internal_date_object: date

    @process(order=0)
    def _ensure_value_is_normalized(self, value: str) -> str:
        """
        Ensures the value object value is normalized date string (ISO 8601, YYYY-MM-DD).

        Args:
            value (str): Value.

        Returns:
            str: Value with the normalized date string.
        """
        return self._internal_date_object.isoformat()

    @validation(order=0)
    def _ensure_value_is_date(self, value: str) -> None:
        """
        Ensures the value object value is a date.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not a date.
        """
        try:
            self._internal_date_object = parse(timestr=value).date()

        except ParserError:
            self._raise_value_is_not_valid_date(value=value)

    def _raise_value_is_not_valid_date(self, value: str) -> NoReturn:
        """
        Raises a ValueError indicating the provided value is not a valid date.

        Args:
            value (str): The invalid date value.

        Raises:
            ValueError: If the value is not a valid date.
        """
        raise ValueError(f'StringDateValueObject value <<<{value}>>> is not a valid date.')

    def is_today(self, *, reference_date: date) -> bool:
        """
        Determines whether the stored date value is today's date.

        Args:
            reference_date (date): The date to compare against.

        Raises:
            TypeError: If the `reference_date` is not a date.

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
        DateValueObject(value=reference_date, title='StringDateValueObject', parameter='reference_date')

        return self._internal_date_object == reference_date

    def is_later_than(self, *, reference_date: date) -> bool:
        """
        Determines whether the stored date value is later than the specified date.

        Args:
            reference_date (date): The date to compare against.

        Raises:
            TypeError: If the `reference_date` is not a date.

        Returns:
            bool: True if the stored date is later than the reference_date, False otherwise.

        Example:
        ```python
        from datetime import date

        from value_object_pattern.usables.dates import StringDateValueObject

        now = '1900-01-01'
        reference_date = date(year=1899, month=12, day=31)
        is_later_than = StringDateValueObject(value=now).is_later_than(reference_date=reference_date)

        print(is_later_than)
        # >>> True
        ```
        """
        DateValueObject(value=reference_date, title='StringDateValueObject', parameter='reference_date')

        return self._internal_date_object > reference_date

    def is_in_range(self, *, start_date: date, end_date: date) -> bool:
        """
        Determines whether the stored date value falls within the specified date range (both included).

        Args:
            start_date (date): The beginning of the date range.
            end_date (date): The end of the date range.

        Raises:
            TypeError: If the `start_date` is not a date.
            TypeError: If the `end_date` is not a date.
            ValueError: If the `start_date` is later than the `end_date`.

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
        DateValueObject(value=start_date, title='StringDateValueObject', parameter='start_date')
        DateValueObject(value=end_date, title='StringDateValueObject', parameter='end_date')

        if start_date > end_date:
            self._raise_start_date_is_later_than_end_date(start_date=start_date, end_date=end_date)

        return start_date <= self._internal_date_object <= end_date

    def _raise_start_date_is_later_than_end_date(self, *, start_date: date, end_date: date) -> NoReturn:
        """
        Raises a ValueError if the start date is later than the end date.

        Args:
            start_date (date): The start date.
            end_date (date): The end date.

        Raises:
            ValueError: If the `start_date` is later than the `end_date`.
        """
        raise ValueError(f'StringDateValueObject start_date <<<{start_date.isoformat()}>>> must be earlier than or equal to end_date <<<{end_date.isoformat()}>>>.')  # noqa: E501  # fmt: skip

    def calculate_age(self, *, reference_date: date) -> int:
        """
        Calculates the age of the stored date value.

        Args:
            reference_date (date): The date to calculate the age from.

        Raises:
            TypeError: If the `reference_date` is not a date.
            ValueError: If the stored date is later than the `reference_date`.

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
        DateValueObject(value=reference_date, title='StringDateValueObject', parameter='reference_date')

        if self._internal_date_object > reference_date:
            self._raise_start_date_is_later_than_end_date(
                start_date=self._internal_date_object,
                end_date=reference_date,
            )

        return relativedelta(dt1=reference_date, dt2=self._internal_date_object).years
