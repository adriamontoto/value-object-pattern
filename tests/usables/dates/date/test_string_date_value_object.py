"""
Test StringDateValueObject value object.
"""

from datetime import date

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.dates import StringDateValueObject


@mark.unit_testing
def test_string_date_value_object_happy_path() -> None:
    """
    Test StringDateValueObject value object happy path.
    """
    date_value = StringDateValueObject(value='2000-05-20')

    assert type(date_value.value) is str
    assert date_value.value == '2000-05-20'


@mark.unit_testing
def test_string_date_value_object_rejects_surrounding_whitespace() -> None:
    """
    Preserve the inherited requirement for already-trimmed input.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StringDateValueObject value <<<  2000-05-20  >>> contains leading or trailing whitespaces\. Only trimmed values are allowed\.',  # noqa: E501
    ):
        StringDateValueObject(value='  2000-05-20  ')


@mark.unit_testing
def test_string_date_value_object_normalizes_basic_iso_date() -> None:
    """
    Normalize a compact ISO date accepted by the standard library.
    """
    assert StringDateValueObject(value='20000520').value == '2000-05-20'


@mark.unit_testing
def test_string_date_value_object_normalizes_iso_week_date() -> None:
    """
    Normalize an ISO week date to its calendar representation.
    """
    assert StringDateValueObject(value='2000-W20-6').value == '2000-05-20'


@mark.unit_testing
def test_string_date_value_object_rejects_human_readable_date() -> None:
    """
    Reject the previously accepted human-readable date format explicitly.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StringDateValueObject value <<<May 20, 2000>>> is not a valid date\.',
    ):
        StringDateValueObject(value='May 20, 2000')


@mark.unit_testing
def test_string_date_value_object_rejects_ambiguous_date() -> None:
    """
    Reject slash-separated dates rather than guessing their component order.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StringDateValueObject value <<<05/06/2000>>> is not a valid date\.',
    ):
        StringDateValueObject(value='05/06/2000')


@mark.unit_testing
def test_string_date_value_object_rejects_incomplete_date() -> None:
    """
    Reject an incomplete date rather than supplying the current day.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StringDateValueObject value <<<2000-05>>> is not a valid date\.',
    ):
        StringDateValueObject(value='2000-05')


@mark.unit_testing
def test_string_date_value_object_rejects_datetime_input() -> None:
    """
    Reject a datetime instead of silently discarding its time component.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StringDateValueObject value <<<2000-05-20T08:30:00>>> is not a valid date\.',
    ):
        StringDateValueObject(value='2000-05-20T08:30:00')


@mark.unit_testing
def test_string_date_value_object_rejects_non_leap_century_day() -> None:
    """
    Reject February 29 in a century that is not a leap year.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StringDateValueObject value <<<1900-02-29>>> is not a valid date\.',
    ):
        StringDateValueObject(value='1900-02-29')


@mark.unit_testing
def test_string_date_value_object_calculate_age_on_leap_day_anniversary() -> None:
    """
    Count the February 28 anniversary of a leap-day birthday in a non-leap year.
    """
    assert StringDateValueObject(value='2000-02-29').calculate_age(reference_date=date(2001, 2, 28)) == 1


@mark.unit_testing
def test_string_date_value_object_invalid_value() -> None:
    """
    Test StringDateValueObject value object raises ValueError when value is not a valid date.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StringDateValueObject value <<<not-a-date>>> is not a valid date.',
    ):
        StringDateValueObject(value='not-a-date')


@mark.unit_testing
def test_string_date_value_object_is_today() -> None:
    """
    Test StringDateValueObject is_today method.
    """
    assert StringDateValueObject(value='2026-05-20').is_today(reference_date=date(year=2026, month=5, day=20))


@mark.unit_testing
def test_string_date_value_object_is_not_today() -> None:
    """
    Test StringDateValueObject is_today method returns false when the dates differ.
    """
    assert not StringDateValueObject(value='2000-05-20').is_today(reference_date=date(year=2026, month=5, day=20))


@mark.unit_testing
def test_string_date_value_object_is_later_than() -> None:
    """
    Test StringDateValueObject is_later_than method.
    """
    assert StringDateValueObject(value='2026-05-20').is_later_than(reference_date=date(year=2000, month=5, day=20))


@mark.unit_testing
def test_string_date_value_object_is_in_range() -> None:
    """
    Test StringDateValueObject is_in_range method.
    """
    assert StringDateValueObject(value='2000-05-20').is_in_range(
        start_date=date(year=2000, month=1, day=1),
        end_date=date(year=2026, month=1, day=1),
    )


@mark.unit_testing
def test_string_date_value_object_is_not_in_range() -> None:
    """
    Test StringDateValueObject is_in_range method returns false when the date is outside the range.
    """
    assert not StringDateValueObject(value='2000-05-20').is_in_range(
        start_date=date(year=2026, month=1, day=1),
        end_date=date(year=2026, month=12, day=31),
    )


@mark.unit_testing
def test_string_date_value_object_is_in_range_start_date_after_end_date() -> None:
    """
    Test StringDateValueObject is_in_range method raises ValueError when start_date is later than end_date.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=(
            r'StringDateValueObject start_date <<<2026-01-01>>> must be earlier than or equal to '
            r'end_date <<<2000-01-01>>>.'
        ),
    ):
        StringDateValueObject(value='2000-05-20').is_in_range(
            start_date=date(year=2026, month=1, day=1),
            end_date=date(year=2000, month=1, day=1),
        )


@mark.unit_testing
def test_string_date_value_object_calculate_age() -> None:
    """
    Test StringDateValueObject calculate_age method.
    """
    assert (
        StringDateValueObject(value='2000-05-20').calculate_age(reference_date=date(year=2026, month=5, day=20)) == 26
    )


@mark.unit_testing
def test_string_date_value_object_calculate_age_start_date_after_reference_date() -> None:
    """
    Test StringDateValueObject calculate_age method raises ValueError when value is later than reference_date.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=(
            r'StringDateValueObject start_date <<<2026-05-20>>> must be earlier than or equal to '
            r'end_date <<<2000-05-20>>>.'
        ),
    ):
        StringDateValueObject(value='2026-05-20').calculate_age(reference_date=date(year=2000, month=5, day=20))
