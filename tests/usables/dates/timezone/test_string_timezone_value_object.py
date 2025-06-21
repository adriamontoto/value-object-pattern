"""
Test StringTimezoneValueObject value object.
"""

from object_mother_pattern.mothers import StringMother
from object_mother_pattern.mothers.dates import StringTimezoneMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.dates import StringTimezoneValueObject


@mark.unit_testing
def test_string_timezone_value_object_happy_path() -> None:
    """
    Test StringTimezoneValueObject value object happy path.
    """
    timezone_value = StringTimezoneValueObject(value=StringTimezoneMother.create())

    assert type(timezone_value.value) is str


@mark.unit_testing
def test_string_timezone_value_object_invalid_type() -> None:
    """
    Test StringTimezoneValueObject value object raises TypeError when value is not string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'StringTimezoneValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        StringTimezoneValueObject(value=StringTimezoneMother.invalid_type())


@mark.unit_testing
def test_string_timezone_value_object_invalid_value() -> None:
    """
    Test StringTimezoneValueObject value object raises ValueError when value is not a string timezone.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StringTimezoneValueObject value <<<.*>>> must be a timezone.',
    ):
        StringTimezoneValueObject(value=StringMother.create())
