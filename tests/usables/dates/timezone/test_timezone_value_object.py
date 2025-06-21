"""
Test TimezoneValueObject value object.
"""

from zoneinfo import ZoneInfo

from object_mother_pattern.mothers.dates import TimezoneMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.dates import TimezoneValueObject


@mark.unit_testing
def test_timezone_value_object_happy_path() -> None:
    """
    Test TimezoneValueObject value object happy path.
    """
    timezone_value = TimezoneValueObject(value=TimezoneMother.create())

    assert isinstance(timezone_value.value, ZoneInfo)


@mark.unit_testing
def test_timezone_value_object_invalid_type() -> None:
    """
    Test TimezoneValueObject value object raises TypeError when value is not string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'TimezoneValueObject value <<<.*>>> must be a timezone. Got <<<.*>>> type.',
    ):
        TimezoneValueObject(value=TimezoneMother.invalid_type())
