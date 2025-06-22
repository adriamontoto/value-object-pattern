"""
Test IntegerValueObject value object.
"""

from object_mother_pattern import IntegerMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables import IntegerValueObject


@mark.unit_testing
def test_integer_value_object_happy_path() -> None:
    """
    Test IntegerValueObject value object happy path.
    """
    integer_value = IntegerValueObject(value=IntegerMother.create())

    assert type(integer_value.value) is int


@mark.unit_testing
def test_integer_value_object_invalid_type() -> None:
    """
    Test IntegerValueObject value object raises TypeError when value is not integer.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'IntegerValueObject value <<<.*>>> must be an integer. Got <<<.*>>> type.',
    ):
        IntegerValueObject(value=IntegerMother.invalid_type())
