"""
Test PositiveIntegerValueObject value object.
"""

from object_mother_pattern.mothers import IntegerMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables import PositiveIntegerValueObject


@mark.unit_testing
def test_positive_integer_value_object_happy_path() -> None:
    """
    Test PositiveIntegerValueObject value object happy path.
    """
    integer_value = PositiveIntegerValueObject(value=IntegerMother.positive())

    assert type(integer_value.value) is int
    assert integer_value.value > 0


@mark.unit_testing
def test_positive_integer_value_object_lower_bound() -> None:
    """
    Test PositiveIntegerValueObject value object lower bound.
    """
    PositiveIntegerValueObject(value=IntegerMother.create(value=1))


@mark.unit_testing
def test_positive_integer_value_object_lower_bound_error() -> None:
    """
    Test PositiveIntegerValueObject value object lower bound error.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'PositiveIntegerValueObject value <<<.*>>> must be a positive integer.',
    ):
        PositiveIntegerValueObject(value=IntegerMother.create(value=0))


@mark.unit_testing
def test_positive_integer_value_object_random_lower_bound_error() -> None:
    """
    Test PositiveIntegerValueObject value object random lower bound error.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'PositiveIntegerValueObject value <<<.*>>> must be a positive integer.',
    ):
        PositiveIntegerValueObject(value=IntegerMother.negative_or_zero())


@mark.unit_testing
def test_positive_integer_value_object_invalid_type() -> None:
    """
    Test PositiveIntegerValueObject value object raises TypeError when value is not integer.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'IntegerValueObject value <<<.*>>> must be an integer. Got <<<.*>>> type.',
    ):
        PositiveIntegerValueObject(value=IntegerMother.invalid_type())
