"""
Test PositiveOrZeroIntegerValueObject value object.
"""

from object_mother_pattern import IntegerMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables import PositiveOrZeroIntegerValueObject


@mark.unit_testing
def test_positive_or_zero_integer_value_object_happy_path() -> None:
    """
    Test PositiveOrZeroIntegerValueObject value object happy path.
    """
    integer_value = PositiveOrZeroIntegerValueObject(value=IntegerMother.positive_or_zero())

    assert type(integer_value.value) is int
    assert integer_value.value >= 0


@mark.unit_testing
def test_positive_or_zero_integer_value_object_lower_bound() -> None:
    """
    Test PositiveOrZeroIntegerValueObject value object lower bound.
    """
    PositiveOrZeroIntegerValueObject(value=IntegerMother.create(value=0))


@mark.unit_testing
def test_positive_or_zero_integer_value_object_lower_bound_error() -> None:
    """
    Test PositiveOrZeroIntegerValueObject value object lower bound error.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'PositiveOrZeroIntegerValueObject value <<<.*>>> must be a positive or zero integer.',
    ):
        PositiveOrZeroIntegerValueObject(value=IntegerMother.create(value=-1))


@mark.unit_testing
def test_positive_or_zero_integer_value_object_random_lower_bound_error() -> None:
    """
    Test PositiveOrZeroIntegerValueObject value object random lower bound error.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'PositiveOrZeroIntegerValueObject value <<<.*>>> must be a positive or zero integer.',
    ):
        PositiveOrZeroIntegerValueObject(value=IntegerMother.negative())


@mark.unit_testing
def test_positive_or_zero_integer_value_object_invalid_type() -> None:
    """
    Test PositiveOrZeroIntegerValueObject value object raises TypeError when value is not integer.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'IntegerValueObject value <<<.*>>> must be an integer. Got <<<.*>>> type.',
    ):
        PositiveOrZeroIntegerValueObject(value=IntegerMother.invalid_type())
