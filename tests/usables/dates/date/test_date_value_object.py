"""
Test DateValueObject value object.
"""

from datetime import date
from typing import Any

from object_mother_pattern import StringMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.dates import DateValueObject


@mark.unit_testing
def test_date_value_object_happy_path() -> None:
    """
    Test DateValueObject value object happy path.
    """
    raw_date = date(year=2000, month=5, day=20)

    date_value = DateValueObject(value=raw_date)

    assert type(date_value.value) is date
    assert date_value.value == raw_date


@mark.unit_testing
def test_date_value_object_invalid_type() -> None:
    """
    Test DateValueObject value object raises TypeError when value is not a date.
    """
    invalid_value: Any = StringMother.create()

    with assert_raises(
        expected_exception=TypeError,
        match=r'DateValueObject value <<<.*>>> must be a date. Got <<<str>>> type.',
    ):
        DateValueObject(value=invalid_value)


@mark.unit_testing
def test_date_value_object_is_today() -> None:
    """
    Test DateValueObject is_today method.
    """
    reference_date = date(year=2026, month=5, day=20)

    assert DateValueObject(value=reference_date).is_today(reference_date=reference_date)


@mark.unit_testing
def test_date_value_object_is_not_today() -> None:
    """
    Test DateValueObject is_today method returns false when the dates differ.
    """
    reference_date = date(year=2026, month=5, day=20)

    assert not DateValueObject(value=date(year=2000, month=5, day=20)).is_today(reference_date=reference_date)


@mark.unit_testing
def test_date_value_object_is_today_invalid_reference_date() -> None:
    """
    Test DateValueObject is_today method raises TypeError when reference_date is not a date.
    """
    invalid_reference_date: Any = StringMother.create()

    with assert_raises(
        expected_exception=TypeError,
        match=r'DateValueObject reference_date <<<.*>>> must be a date. Got <<<str>>> type.',
    ):
        DateValueObject(value=date(year=2026, month=5, day=20)).is_today(reference_date=invalid_reference_date)


@mark.unit_testing
def test_date_value_object_is_later_than() -> None:
    """
    Test DateValueObject is_later_than method.
    """
    assert DateValueObject(value=date(year=2026, month=5, day=20)).is_later_than(
        reference_date=date(year=2000, month=5, day=20),
    )


@mark.unit_testing
def test_date_value_object_is_in_range() -> None:
    """
    Test DateValueObject is_in_range method.
    """
    assert DateValueObject(value=date(year=2000, month=5, day=20)).is_in_range(
        start_date=date(year=2000, month=1, day=1),
        end_date=date(year=2026, month=1, day=1),
    )


@mark.unit_testing
def test_date_value_object_is_not_in_range() -> None:
    """
    Test DateValueObject is_in_range method returns false when the date is outside the range.
    """
    assert not DateValueObject(value=date(year=2000, month=5, day=20)).is_in_range(
        start_date=date(year=2026, month=1, day=1),
        end_date=date(year=2026, month=5, day=20),
    )


@mark.unit_testing
def test_date_value_object_is_in_range_start_date_after_end_date() -> None:
    """
    Test DateValueObject is_in_range method raises ValueError when start_date is later than end_date.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=(
            r'DateValueObject start_date <<<2026-05-20>>> must be earlier than or equal to '
            r'end_date <<<2000-05-20>>>.'
        ),
    ):
        DateValueObject(value=date(year=2000, month=5, day=20)).is_in_range(
            start_date=date(year=2026, month=5, day=20),
            end_date=date(year=2000, month=5, day=20),
        )


@mark.unit_testing
def test_date_value_object_calculate_age() -> None:
    """
    Test DateValueObject calculate_age method.
    """
    assert (
        DateValueObject(value=date(year=2000, month=5, day=20)).calculate_age(
            reference_date=date(year=2026, month=5, day=20),
        )
        == 26
    )


@mark.unit_testing
def test_date_value_object_calculate_age_start_date_after_reference_date() -> None:
    """
    Test DateValueObject calculate_age method raises ValueError when value is later than reference_date.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=(
            r'DateValueObject start_date <<<2026-05-20>>> must be earlier than or equal to '
            r'end_date <<<2000-05-20>>>.'
        ),
    ):
        DateValueObject(value=date(year=2026, month=5, day=20)).calculate_age(
            reference_date=date(year=2000, month=5, day=20),
        )
