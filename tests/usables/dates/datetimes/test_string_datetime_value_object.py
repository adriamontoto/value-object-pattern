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
def test_string_datetime_value_object_normalizes_z_and_fractional_seconds() -> None:
    """
    Preserve microseconds and normalize the ISO UTC suffix.
    """
    assert StringDatetimeValueObject(value='2000-05-20T08:30:00.123456Z').value == '2000-05-20T08:30:00.123456+00:00'


@mark.unit_testing
def test_string_datetime_value_object_normalizes_positive_offset_across_day_boundary() -> None:
    """
    Convert an ISO datetime with a positive offset to the previous UTC day.
    """
    assert StringDatetimeValueObject(value='2000-05-20T00:30:00+14:00').value == '2000-05-19T10:30:00+00:00'


@mark.unit_testing
def test_string_datetime_value_object_normalizes_negative_offset_across_day_boundary() -> None:
    """
    Convert an ISO datetime with a fractional-hour negative offset to the next UTC day.
    """
    assert StringDatetimeValueObject(value='2000-05-20T23:30:00-05:45').value == '2000-05-21T05:15:00+00:00'


@mark.unit_testing
def test_string_datetime_value_object_rejects_surrounding_whitespace() -> None:
    """
    Preserve the inherited requirement for already-trimmed input.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StringDatetimeValueObject value <<<  2000-05-20T08:30:00\+00:00  >>> contains leading or trailing whitespaces\. Only trimmed values are allowed\.',  # noqa: E501
    ):
        StringDatetimeValueObject(value='  2000-05-20T08:30:00+00:00  ')


@mark.unit_testing
def test_string_datetime_value_object_rejects_human_readable_datetime() -> None:
    """
    Reject a human-readable datetime instead of using a permissive parser.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StringDatetimeValueObject value <<<May 20, 2000 08:30:00>>> is not a valid datetime\.',
    ):
        StringDatetimeValueObject(value='May 20, 2000 08:30:00')


@mark.unit_testing
def test_string_datetime_value_object_rejects_non_leap_century_day() -> None:
    """
    Preserve the public validation error for an impossible ISO datetime.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StringDatetimeValueObject value <<<1900-02-29T08:30:00Z>>> is not a valid datetime\.',
    ):
        StringDatetimeValueObject(value='1900-02-29T08:30:00Z')


@mark.unit_testing
def test_string_datetime_value_object_rejects_end_of_day_hour() -> None:
    """
    Reject hour 24 consistently even on Python versions whose ISO parser accepts it.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StringDatetimeValueObject value <<<2024-01-01T24:00:00Z>>> is not a valid datetime\.',
    ):
        StringDatetimeValueObject(value='2024-01-01T24:00:00Z')


@mark.unit_testing
def test_string_datetime_value_object_rejects_fractional_hour() -> None:
    """
    Reject fractional-hour input consistently across Python parser versions.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StringDatetimeValueObject value <<<2024-01-01T12\.5Z>>> is not a valid datetime\.',
    ):
        StringDatetimeValueObject(value='2024-01-01T12.5Z')


@mark.unit_testing
def test_string_datetime_value_object_rejects_fractional_minute() -> None:
    """
    Require seconds before accepting a fractional time component.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StringDatetimeValueObject value <<<2024-01-01T12:30\.5Z>>> is not a valid datetime\.',
    ):
        StringDatetimeValueObject(value='2024-01-01T12:30.5Z')


@mark.unit_testing
def test_string_datetime_value_object_rejects_arbitrary_separator() -> None:
    """
    Reject separator characters outside the supported ISO contract.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StringDatetimeValueObject value <<<2024-01-01X12:30:00Z>>> is not a valid datetime\.',
    ):
        StringDatetimeValueObject(value='2024-01-01X12:30:00Z')


@mark.unit_testing
def test_string_datetime_value_object_normalizes_compact_iso_datetime() -> None:
    """
    Normalize compact ISO calendar dates and compact times.
    """
    assert StringDatetimeValueObject(value='20000520T083000Z').value == '2000-05-20T08:30:00+00:00'


@mark.unit_testing
def test_string_datetime_value_object_normalizes_iso_week_datetime() -> None:
    """
    Normalize an ISO week datetime with a fractional-second numeric offset.
    """
    assert StringDatetimeValueObject(value='2000-W20-6T08:30:00+02:30:15.5').value == '2000-05-20T05:59:44.500000+00:00'


@mark.unit_testing
def test_string_datetime_value_object_normalizes_lowercase_separator_and_compact_offset() -> None:
    """
    Accept a lowercase separator and a compact numeric timezone offset.
    """
    assert StringDatetimeValueObject(value='2000-05-20t08:30:00+0230').value == '2000-05-20T06:00:00+00:00'


@mark.unit_testing
def test_string_datetime_value_object_calculate_age_on_leap_day_anniversary() -> None:
    """
    Preserve the time of day when counting a leap-day anniversary.
    """
    assert (
        StringDatetimeValueObject(value='2000-02-29T08:30:00Z').calculate_age(
            reference_datetime=datetime(2001, 2, 28, 8, 30, tzinfo=UTC),
        )
        == 1
    )


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
