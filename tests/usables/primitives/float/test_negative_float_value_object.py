"""
Test NegativeFloatValueObject value object.
"""

from object_mother_pattern import FloatMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.primitives.float import NegativeFloatValueObject


@mark.unit_testing
def test_negative_float_value_object_happy_path() -> None:
    """
    Test NegativeFloatValueObject value object happy path.
    """
    value_object = NegativeFloatValueObject(value=FloatMother.negative())

    assert type(value_object.value) is float
    assert value_object.value < 0.0


@mark.unit_testing
def test_negative_float_value_object_lower_bound() -> None:
    """
    Test NegativeFloatValueObject value object lower bound.
    """
    NegativeFloatValueObject(value=FloatMother.create(value=-0.000001))


@mark.unit_testing
def test_negative_float_value_object_lower_bound_error() -> None:
    """
    Test NegativeFloatValueObject value object lower bound error.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'NegativeFloatValueObject value <<<.*>>> must be a negative float.',
    ):
        NegativeFloatValueObject(value=FloatMother.create(value=0.0))


@mark.unit_testing
def test_negative_float_value_object_random_lower_bound_error() -> None:
    """
    Test NegativeFloatValueObject value object random lower bound error.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'NegativeFloatValueObject value <<<.*>>> must be a negative float.',
    ):
        NegativeFloatValueObject(value=FloatMother.positive_or_zero())


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
