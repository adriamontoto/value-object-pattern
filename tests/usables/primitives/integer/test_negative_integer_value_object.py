"""
Test NegativeIntegerValueObject value object.
"""

from object_mother_pattern.mothers import IntegerMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.primitives import NegativeIntegerValueObject


@mark.unit_testing
def test_negative_integer_value_object_happy_path() -> None:
    """
    Test NegativeIntegerValueObject value object happy path.
    """
    integer_value = NegativeIntegerValueObject(value=IntegerMother.negative())

    assert type(integer_value.value) is int
    assert integer_value.value < 0


@mark.unit_testing
def test_negative_integer_value_object_invalid_value() -> None:
    """
    Test NegativeIntegerValueObject value object raises ValueError when value is not negative.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'NegativeIntegerValueObject value <<<.*>>> must be a negative integer.',
    ):
        NegativeIntegerValueObject(value=IntegerMother.create(min=0))


@mark.unit_testing
def test_negative_integer_value_object_invalid_type() -> None:
    """
    Test NegativeIntegerValueObject value object raises TypeError when value is not integer.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'IntegerValueObject value <<<.*>>> must be an integer. Got <<<.*>>> type.',
    ):
        NegativeIntegerValueObject(value=IntegerMother.invalid_type())
