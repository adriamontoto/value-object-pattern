"""
Test NegativeOrZeroIntegerValueObject value object.
"""

from object_mother_pattern import IntegerMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables import NegativeOrZeroIntegerValueObject


@mark.unit_testing
def test_negative_or_zero_integer_value_object_happy_path() -> None:
    """
    Test NegativeOrZeroIntegerValueObject value object happy path.
    """
    integer_value = NegativeOrZeroIntegerValueObject(value=IntegerMother.negative_or_zero())

    assert type(integer_value.value) is int
    assert integer_value.value <= 0


@mark.unit_testing
def test_negative_or_zero_integer_value_object_upper_bound() -> None:
    """
    Test NegativeOrZeroIntegerValueObject value object upper bound.
    """
    NegativeOrZeroIntegerValueObject(value=IntegerMother.create(value=0))


@mark.unit_testing
def test_negative_or_zero_integer_value_object_upper_bound_error() -> None:
    """
    Test NegativeOrZeroIntegerValueObject value object upper bound error.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'NegativeOrZeroIntegerValueObject value <<<.*>>> must be a negative or zero integer.',
    ):
        NegativeOrZeroIntegerValueObject(value=IntegerMother.create(value=1))


@mark.unit_testing
def test_negative_or_zero_integer_value_object_random_upper_bound_error() -> None:
    """
    Test NegativeOrZeroIntegerValueObject value object random upper bound error.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'NegativeOrZeroIntegerValueObject value <<<.*>>> must be a negative or zero integer.',
    ):
        NegativeOrZeroIntegerValueObject(value=IntegerMother.positive())


@mark.unit_testing
def test_negative_or_zero_integer_value_object_invalid_type() -> None:
    """
    Test NegativeOrZeroIntegerValueObject value object raises TypeError when value is not integer.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'IntegerValueObject value <<<.*>>> must be an integer. Got <<<.*>>> type.',
    ):
        NegativeOrZeroIntegerValueObject(value=IntegerMother.invalid_type())
