"""
DateValueObject value object.
"""

from datetime import date
from typing import Any, NoReturn

from dateutil.relativedelta import relativedelta

from value_object_pattern.decorators import validation
from value_object_pattern.models import ValueObject


class DateValueObject(ValueObject[date]):
    """
    DateValueObject value object ensures the provided value is a date.

    Example:
    ```python
    from datetime import date

    from value_object_pattern.usables.dates import DateValueObject

    now = date(year=1900, month=1, day=1)
    date_ = DateValueObject(value=datetime.date(1900, 1, 1))

    print(repr(date_))
    # >>> DateValueObject(value=datetime.date(1900, 1, 1))
    ```
    """

    @validation(order=0)
    def _ensure_value_is_date(self, value: date) -> None:
        """
        Ensures the value object `value` is a date.

        Args:
            value (date): Provided value.

        Raises:
            TypeError: If the `value` is not a date.
        """
        if type(value) is not date:
            self._raise_value_is_not_date(value=value)

    def _raise_value_is_not_date(self, value: Any) -> NoReturn:
        """
        Raises a TypeError if the value object `value` is not a date.

        Args:
            value (Any): The provided value.

        Raises:
            TypeError: If the `value` is not a date.
        """
        raise TypeError(f'DateValueObject value <<<{value}>>> must be a date. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip

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

        from value_object_pattern.usables.dates import DateValueObject

        now = date(year=1900, month=1, day=1)
        today = date(year=1900, month=1, day=1)
        is_today = DateValueObject(value=now).is_today(reference_date=today)

        print(is_today)
        # >>> True
        ```
        """
        DateValueObject(value=reference_date, parameter='reference_date')

        return self.value == reference_date

    def is_later_than(self, *, reference_date: date) -> bool:
        """
        Determines whether the stored date value is later than the specified date (same day not included).

        Args:
            reference_date (date): The date to compare against.

        Raises:
            TypeError: If the `reference_date` is not a date.

        Returns:
            bool: True if the stored date is later than the `reference_date`, False otherwise.

        Example:
        ```python
        from datetime import date

        from value_object_pattern.usables.dates import DateValueObject

        now = date(year=1900, month=1, day=1)
        reference_date = date(year=1899, month=12, day=31)
        is_later_than = DateValueObject(value=now).is_later_than(reference_date=reference_date)

        print(is_later_than)
        # >>> True
        ```
        """
        DateValueObject(value=reference_date, parameter='reference_date')

        return self.value > reference_date

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

        from value_object_pattern.usables.dates import DateValueObject

        now = date(year=1900, month=1, day=1)
        start_date = date(year=1899, month=12, day=31)
        end_date = date(year=1900, month=1, day=2)
        is_in_range = DateValueObject(
            value=now,
        ).is_in_range(
            start_date=start_date,
            end_date=end_date,
        )

        print(is_in_range)
        # >>> True
        ```
        """
        DateValueObject(value=start_date, parameter='start_date')
        DateValueObject(value=end_date, parameter='end_date')

        if start_date > end_date:
            self._raise_start_date_is_later_than_end_date(start_date=start_date, end_date=end_date)  # noqa: E501  # fmt: skip

        return start_date <= self.value <= end_date

    def _raise_start_date_is_later_than_end_date(self, *, start_date: date, end_date: date) -> NoReturn:
        """
        Raises a ValueError if the start date is later than the end date.

        Args:
            start_date (date): The start date.
            end_date (date): The end date.

        Raises:
            ValueError: If the `start_date` is later than the `end_date`.
        """
        raise ValueError(f'DateValueObject start_date <<<{start_date.isoformat()}>>> must be earlier than or equal to end_date <<<{end_date.isoformat()}>>>.')  # noqa: E501  # fmt: skip

    def calculate_age(self, *, reference_date: date) -> int:
        """
        Calculates the age of the stored date value.

        Args:
            reference_date (date): The date to calculate the age against.

        Raises:
            TypeError: If the `reference_date` is not a date.
            ValueError: If the stored date is later than the `reference_date`.

        Returns:
            int: The age in years of the stored date.

        Example:
        ```python
        from datetime import date

        from value_object_pattern.usables.dates import DateValueObject

        now = date(year=1900, month=1, day=1)
        today = date(year=2000, month=1, day=1)
        age = DateValueObject(value=now).calculate_age(reference_date=today)

        print(age)
        # >>> 100
        ```
        """
        DateValueObject(value=reference_date, parameter='reference_date')

        if self.value > reference_date:
            self._raise_start_date_is_later_than_end_date(start_date=self.value, end_date=reference_date)

        return relativedelta(dt1=reference_date, dt2=self.value).years
