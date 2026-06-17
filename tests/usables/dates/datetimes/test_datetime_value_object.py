"""
Test DatetimeValueObject value object.
"""

from datetime import UTC, date, datetime
from typing import Any

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.dates import DatetimeValueObject


@mark.unit_testing
def test_datetime_value_object_happy_path() -> None:
    """
    Test DatetimeValueObject value object happy path.
    """
    raw_datetime = datetime(year=2000, month=5, day=20, hour=8, minute=30, tzinfo=UTC)

    datetime_value = DatetimeValueObject(value=raw_datetime)

    assert type(datetime_value.value) is datetime
    assert datetime_value.value == raw_datetime


@mark.unit_testing
def test_datetime_value_object_invalid_type() -> None:
    """
    Test DatetimeValueObject value object raises TypeError when value is not a datetime.
    """
    invalid_value: Any = date(year=2026, month=5, day=20)

    with assert_raises(
        expected_exception=TypeError,
        match=r'DatetimeValueObject value <<<.*>>> must be a datetime. Got <<<date>>> type.',
    ):
        DatetimeValueObject(value=invalid_value)


@mark.unit_testing
def test_datetime_value_object_is_now() -> None:
    """
    Test DatetimeValueObject is_now method.
    """
    reference_datetime = datetime(year=2026, month=5, day=20, hour=9, tzinfo=UTC)

    assert DatetimeValueObject(value=reference_datetime).is_now(reference_datetime=reference_datetime)


@mark.unit_testing
def test_datetime_value_object_is_not_now() -> None:
    """
    Test DatetimeValueObject is_now method returns false when the datetimes differ.
    """
    reference_datetime = datetime(year=2026, month=5, day=20, hour=9, tzinfo=UTC)

    assert not DatetimeValueObject(
        value=datetime(year=2000, month=5, day=20, hour=8, minute=30, tzinfo=UTC),
    ).is_now(reference_datetime=reference_datetime)


@mark.unit_testing
def test_datetime_value_object_is_now_invalid_reference_datetime() -> None:
    """
    Test DatetimeValueObject is_now method raises TypeError when reference_datetime is not a datetime.
    """
    invalid_reference_datetime: Any = date(year=2026, month=5, day=20)

    with assert_raises(
        expected_exception=TypeError,
        match=r'DatetimeValueObject reference_datetime <<<.*>>> must be a datetime. Got <<<date>>> type.',
    ):
        DatetimeValueObject(value=datetime(year=2026, month=5, day=20, hour=9, tzinfo=UTC)).is_now(
            reference_datetime=invalid_reference_datetime,
        )


@mark.unit_testing
def test_datetime_value_object_is_today() -> None:
    """
    Test DatetimeValueObject is_today method.
    """
    datetime_value = DatetimeValueObject(value=datetime(year=2000, month=5, day=20, hour=8, minute=30, tzinfo=UTC))

    assert datetime_value.is_today(reference_datetime=datetime(year=2000, month=5, day=20, hour=23, tzinfo=UTC))


@mark.unit_testing
def test_datetime_value_object_is_later_than() -> None:
    """
    Test DatetimeValueObject is_later_than method.
    """
    assert DatetimeValueObject(value=datetime(year=2026, month=5, day=20, hour=9, tzinfo=UTC)).is_later_than(
        reference_datetime=datetime(year=2000, month=5, day=20, hour=8, tzinfo=UTC),
    )


@mark.unit_testing
def test_datetime_value_object_is_in_range() -> None:
    """
    Test DatetimeValueObject is_in_range method.
    """
    assert DatetimeValueObject(value=datetime(year=2000, month=5, day=20, hour=8, minute=30, tzinfo=UTC)).is_in_range(
        start_datetime=datetime(year=2000, month=1, day=1, tzinfo=UTC),
        end_datetime=datetime(year=2026, month=1, day=1, tzinfo=UTC),
    )


@mark.unit_testing
def test_datetime_value_object_is_not_in_range() -> None:
    """
    Test DatetimeValueObject is_in_range method returns false when the datetime is outside the range.
    """
    assert not DatetimeValueObject(
        value=datetime(year=2000, month=5, day=20, hour=8, minute=30, tzinfo=UTC),
    ).is_in_range(
        start_datetime=datetime(year=2026, month=1, day=1, tzinfo=UTC),
        end_datetime=datetime(year=2026, month=5, day=20, hour=9, tzinfo=UTC),
    )


@mark.unit_testing
def test_datetime_value_object_is_in_range_start_datetime_after_end_datetime() -> None:
    """
    Test DatetimeValueObject is_in_range method raises ValueError when start_datetime is later than end_datetime.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=(
            r'DatetimeValueObject start_datetime <<<2026-05-20T09:00:00\+00:00>>> must be earlier than or equal to '
            r'end_datetime <<<2000-05-20T08:30:00\+00:00>>>.'
        ),
    ):
        DatetimeValueObject(value=datetime(year=2000, month=5, day=20, hour=8, minute=30, tzinfo=UTC)).is_in_range(
            start_datetime=datetime(year=2026, month=5, day=20, hour=9, tzinfo=UTC),
            end_datetime=datetime(year=2000, month=5, day=20, hour=8, minute=30, tzinfo=UTC),
        )


@mark.unit_testing
def test_datetime_value_object_calculate_age() -> None:
    """
    Test DatetimeValueObject calculate_age method.
    """
    assert (
        DatetimeValueObject(value=datetime(year=2000, month=5, day=20, hour=8, minute=30, tzinfo=UTC)).calculate_age(
            reference_datetime=datetime(year=2026, month=5, day=20, hour=9, tzinfo=UTC),
        )
        == 26
    )


@mark.unit_testing
def test_datetime_value_object_calculate_age_start_datetime_after_reference_datetime() -> None:
    """
    Test DatetimeValueObject calculate_age method raises ValueError when value is later than reference_datetime.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=(
            r'DatetimeValueObject start_datetime <<<2026-05-20T09:00:00\+00:00>>> must be earlier than or equal to '
            r'end_datetime <<<2000-05-20T08:30:00\+00:00>>>.'
        ),
    ):
        DatetimeValueObject(value=datetime(year=2026, month=5, day=20, hour=9, tzinfo=UTC)).calculate_age(
            reference_datetime=datetime(year=2000, month=5, day=20, hour=8, minute=30, tzinfo=UTC),
        )
