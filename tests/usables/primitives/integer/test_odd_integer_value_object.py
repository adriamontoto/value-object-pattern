"""
Test OddIntegerValueObject value object.
"""

from object_mother_pattern.mothers import IntegerMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables import OddIntegerValueObject


@mark.unit_testing
def test_odd_integer_value_object_happy_path() -> None:
    """
    Test OddIntegerValueObject value object happy path.
    """
    integer_value = OddIntegerValueObject(value=IntegerMother.create() * 2 + 1)

    assert type(integer_value.value) is int


@mark.unit_testing
def test_odd_integer_value_object_invalid_value() -> None:
    """
    Test OddIntegerValueObject value object raises ValueError when value is not an odd number.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'OddIntegerValueObject value <<<.*>>> must be an odd number.',
    ):
        OddIntegerValueObject(value=IntegerMother.create() * 2)


@mark.unit_testing
def test_odd_integer_value_object_invalid_type() -> None:
    """
    Test OddIntegerValueObject value object raises TypeError when value is not integer.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'IntegerValueObject value <<<.*>>> must be an integer. Got <<<.*>>> type.',
    ):
        OddIntegerValueObject(value=IntegerMother.invalid_type())
