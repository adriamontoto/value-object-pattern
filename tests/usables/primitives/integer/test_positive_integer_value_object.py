"""
Test PositiveIntegerValueObject value object.
"""

from object_mother_pattern.mothers import IntegerMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.primitives import PositiveIntegerValueObject


@mark.unit_testing
def test_positive_integer_value_object_happy_path() -> None:
    """
    Test PositiveIntegerValueObject value object happy path.
    """
    integer_value = PositiveIntegerValueObject(value=IntegerMother.positive())

    assert type(integer_value.value) is int
    assert integer_value.value > 0


@mark.unit_testing
def test_positive_integer_value_object_invalid_value() -> None:
    """
    Test PositiveIntegerValueObject value object raises ValueError when value is not positive.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'PositiveIntegerValueObject value <<<.*>>> must be a positive integer.',
    ):
        PositiveIntegerValueObject(value=IntegerMother.create(max=0))


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
