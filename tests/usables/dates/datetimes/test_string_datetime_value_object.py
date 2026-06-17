"""
Test StringDatetimeValueObject value object.
"""

from datetime import UTC, datetime

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.dates import StringDatetimeValueObject


@mark.unit_testing
def test_string_datetime_value_object_happy_path() -> None:
    """
    Test StringDatetimeValueObject value object happy path.
    """
    datetime_value = StringDatetimeValueObject(value='2000-05-20T08:30:00+00:00')

    assert type(datetime_value.value) is str
    assert datetime_value.value == '2000-05-20T08:30:00+00:00'


@mark.unit_testing
def test_string_datetime_value_object_invalid_value() -> None:
    """
    Test StringDatetimeValueObject value object raises ValueError when value is not a valid datetime.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StringDatetimeValueObject value <<<not-a-datetime>>> is not a valid datetime.',
    ):
        StringDatetimeValueObject(value='not-a-datetime')


@mark.unit_testing
def test_string_datetime_value_object_is_now() -> None:
    """
    Test StringDatetimeValueObject is_now method.
    """
    assert StringDatetimeValueObject(value='2026-05-20T09:00:00+00:00').is_now(
        reference_datetime=datetime(year=2026, month=5, day=20, hour=9, tzinfo=UTC),
    )


@mark.unit_testing
def test_string_datetime_value_object_is_today() -> None:
    """
    Test StringDatetimeValueObject is_today method.
    """
    assert StringDatetimeValueObject(value='2000-05-20T08:30:00+00:00').is_today(
        reference_datetime=datetime(year=2000, month=5, day=20, hour=23, tzinfo=UTC),
    )


@mark.unit_testing
def test_string_datetime_value_object_is_later_than() -> None:
    """
    Test StringDatetimeValueObject is_later_than method.
    """
    assert StringDatetimeValueObject(value='2026-05-20T09:00:00+00:00').is_later_than(
        reference_datetime=datetime(year=2000, month=5, day=20, hour=8, tzinfo=UTC),
    )


@mark.unit_testing
def test_string_datetime_value_object_is_in_range() -> None:
    """
    Test StringDatetimeValueObject is_in_range method.
    """
    assert StringDatetimeValueObject(value='2000-05-20T08:30:00+00:00').is_in_range(
        start_datetime=datetime(year=2000, month=1, day=1, tzinfo=UTC),
        end_datetime=datetime(year=2026, month=5, day=20, hour=9, tzinfo=UTC),
    )


@mark.unit_testing
def test_string_datetime_value_object_is_not_in_range() -> None:
    """
    Test StringDatetimeValueObject is_in_range method returns false when the datetime is outside the range.
    """
    assert not StringDatetimeValueObject(value='2000-05-20T08:30:00+00:00').is_in_range(
        start_datetime=datetime(year=2026, month=1, day=1, tzinfo=UTC),
        end_datetime=datetime(year=2026, month=5, day=20, hour=9, tzinfo=UTC),
    )


@mark.unit_testing
def test_string_datetime_value_object_is_in_range_start_datetime_after_end_datetime() -> None:
    """
    Test StringDatetimeValueObject is_in_range method raises ValueError when start_datetime is later than end_datetime.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=(
            r'StringDatetimeValueObject start_datetime <<<2026-05-20T09:00:00\+00:00>>> must be earlier than '
            r'or equal to end_datetime <<<2000-05-20T00:00:00\+00:00>>>.'
        ),
    ):
        StringDatetimeValueObject(value='2000-05-20T08:30:00+00:00').is_in_range(
            start_datetime=datetime(year=2026, month=5, day=20, hour=9, tzinfo=UTC),
            end_datetime=datetime(year=2000, month=5, day=20, tzinfo=UTC),
        )


@mark.unit_testing
def test_string_datetime_value_object_calculate_age() -> None:
    """
    Test StringDatetimeValueObject calculate_age method.
    """
    assert (
        StringDatetimeValueObject(value='2000-05-20T08:30:00+00:00').calculate_age(
            reference_datetime=datetime(year=2026, month=5, day=20, hour=9, tzinfo=UTC),
        )
        == 26
    )


@mark.unit_testing
def test_string_datetime_value_object_calculate_age_start_datetime_after_reference_datetime() -> None:
    """
    Test StringDatetimeValueObject calculate_age method raises ValueError when value is later than reference_datetime.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=(
            r'StringDatetimeValueObject start_datetime <<<2026-05-20T09:00:00\+00:00>>> must be earlier than '
            r'or equal to end_datetime <<<2000-05-20T08:30:00\+00:00>>>.'
        ),
    ):
        StringDatetimeValueObject(value='2026-05-20T09:00:00+00:00').calculate_age(
            reference_datetime=datetime(year=2000, month=5, day=20, hour=8, minute=30, tzinfo=UTC),
        )
