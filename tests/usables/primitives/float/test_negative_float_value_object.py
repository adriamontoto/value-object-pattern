"""
Test NegativeFloatValueObject value object.
"""

from object_mother_pattern.mothers import FloatMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.primitives import NegativeFloatValueObject


@mark.unit_testing
def test_negative_float_value_object_happy_path() -> None:
    """
    Test NegativeFloatValueObject value object happy path.
    """
    float_value = NegativeFloatValueObject(value=FloatMother.negative())

    assert type(float_value.value) is float
    assert float_value.value < 0


@mark.unit_testing
def test_negative_float_value_object_invalid_value() -> None:
    """
    Test NegativeFloatValueObject value object raises ValueError when value is not negative.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'NegativeFloatValueObject value <<<.*>>> must be a negative float.',
    ):
        NegativeFloatValueObject(value=FloatMother.create(min=0))


@mark.unit_testing
def test_negative_float_value_object_invalid_type() -> None:
    """
    Test NegativeFloatValueObject value object raises TypeError when value is not float.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'FloatValueObject value <<<.*>>> must be a float. Got <<<.*>>> type.',
    ):
        NegativeFloatValueObject(value=FloatMother.invalid_type())
