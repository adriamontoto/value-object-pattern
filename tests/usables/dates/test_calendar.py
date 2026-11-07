"""
Regression tests for completed calendar years through the public value objects.
"""

from datetime import UTC, date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from pytest import mark

from value_object_pattern.usables.dates import DateValueObject, DatetimeValueObject


@mark.unit_testing
def test_calculate_age_before_first_anniversary() -> None:
    """
    Count no completed years during the first calendar year.
    """
    assert DateValueObject(value=date(2000, 5, 20)).calculate_age(reference_date=date(2000, 12, 31)) == 0


@mark.unit_testing
def test_calculate_age_before_birthday() -> None:
    """
    Exclude an anniversary that has not occurred yet.
    """
    assert DateValueObject(value=date(2000, 5, 20)).calculate_age(reference_date=date(2026, 5, 19)) == 25


@mark.unit_testing
def test_calculate_age_clamps_leap_day_in_non_leap_year() -> None:
    """
    Count February 28 as the anniversary of February 29 in a non-leap year.
    """
    assert DateValueObject(value=date(2000, 2, 29)).calculate_age(reference_date=date(2001, 2, 28)) == 1


@mark.unit_testing
def test_calculate_age_keeps_leap_day_in_leap_year() -> None:
    """
    Wait until February 29 when the reference year is also a leap year.
    """
    assert DateValueObject(value=date(2000, 2, 29)).calculate_age(reference_date=date(2004, 2, 28)) == 3


@mark.unit_testing
def test_calculate_age_handles_non_leap_century() -> None:
    """
    Clamp an anniversary in 1900 even though 1896 was a leap year.
    """
    assert DateValueObject(value=date(1896, 2, 29)).calculate_age(reference_date=date(1900, 2, 28)) == 4


@mark.unit_testing
def test_calculate_age_keeps_microsecond_boundary() -> None:
    """
    Exclude the anniversary one microsecond before its original time of day.
    """
    assert (
        DatetimeValueObject(value=datetime(2000, 5, 20, 8, 30, microsecond=1, tzinfo=UTC)).calculate_age(
            reference_datetime=datetime(2026, 5, 20, 8, 30, tzinfo=UTC),
        )
        == 25
    )


@mark.unit_testing
def test_calculate_age_preserves_reference_calendar_month_with_different_offsets() -> None:
    """
    Preserve the calendar-month upper bound even when offsets move the reference past an anniversary instant.
    """
    assert (
        DatetimeValueObject(value=datetime(2000, 3, 1, tzinfo=timezone(timedelta(hours=14)))).calculate_age(
            reference_datetime=datetime(2001, 2, 28, 12, tzinfo=timezone(timedelta(hours=-12))),
        )
        == 0
    )


@mark.unit_testing
def test_calculate_age_handles_ordered_datetimes_with_reversed_local_months() -> None:
    """
    Count zero years for ordered instants whose local month fields run backwards.
    """
    assert (
        DatetimeValueObject(value=datetime(2000, 3, 1, tzinfo=timezone(timedelta(hours=14)))).calculate_age(
            reference_datetime=datetime(2000, 2, 29, 23, tzinfo=timezone(timedelta(hours=-12))),
        )
        == 0
    )


@mark.unit_testing
def test_calculate_age_preserves_daylight_saving_fold_behavior() -> None:
    """
    Preserve calendar-offset behavior when a repeated local time is the anniversary.
    """
    assert (
        DatetimeValueObject(
            value=datetime(2019, 10, 27, 2, 30, tzinfo=ZoneInfo('Europe/Berlin'), fold=1)
        ).calculate_age(
            reference_datetime=datetime(2024, 10, 27, 1, tzinfo=UTC),
        )
        == 5
    )
