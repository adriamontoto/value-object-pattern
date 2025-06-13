"""
Test EvenIntegerValueObject value object.
"""

from object_mother_pattern.mothers import IntegerMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables import EvenIntegerValueObject


@mark.unit_testing
def test_even_integer_value_object_happy_path() -> None:
    """
    Test EvenIntegerValueObject value object happy path.
    """
    integer_value = EvenIntegerValueObject(value=IntegerMother.create() * 2)

    assert type(integer_value.value) is int


@mark.unit_testing
def test_even_integer_value_object_invalid_value() -> None:
    """
    Test EvenIntegerValueObject value object raises ValueError when value is not an even number.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'EvenIntegerValueObject value <<<.*>>> must be an even number.',
    ):
        EvenIntegerValueObject(value=IntegerMother.create() * 2 + 1)


@mark.unit_testing
def test_even_integer_value_object_invalid_type() -> None:
    """
    Test EvenIntegerValueObject value object raises TypeError when value is not integer.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'IntegerValueObject value <<<.*>>> must be an integer. Got <<<.*>>> type.',
    ):
        EvenIntegerValueObject(value=IntegerMother.invalid_type())
