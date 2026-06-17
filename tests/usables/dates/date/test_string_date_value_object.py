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
    date_value = StringDateValueObject(value='May 20, 2000')

    assert type(date_value.value) is str
    assert date_value.value == '2000-05-20'


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
