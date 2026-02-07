"""
Test NegativeOrZeroFloatValueObject value object.
"""

from object_mother_pattern import FloatMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.primitives.float import NegativeOrZeroFloatValueObject


@mark.unit_testing
def test_negative_or_zero_float_value_object_happy_path() -> None:
    """
    Test NegativeOrZeroFloatValueObject value object happy path.
    """
    value_object = NegativeOrZeroFloatValueObject(value=FloatMother.negative_or_zero())

    assert type(value_object.value) is float
    assert value_object.value <= 0.0


@mark.unit_testing
def test_negative_or_zero_float_value_object_upper_bound() -> None:
    """
    Test NegativeOrZeroFloatValueObject value object upper bound.
    """
    NegativeOrZeroFloatValueObject(value=FloatMother.create(value=0.0))


@mark.unit_testing
def test_negative_or_zero_float_value_object_upper_bound_error() -> None:
    """
    Test NegativeOrZeroFloatValueObject value object upper bound error.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'NegativeOrZeroFloatValueObject value <<<.*>>> must be a negative or zero float.',
    ):
        NegativeOrZeroFloatValueObject(value=FloatMother.create(value=0.000001))


@mark.unit_testing
def test_negative_or_zero_float_value_object_random_upper_bound_error() -> None:
    """
    Test NegativeOrZeroFloatValueObject value object random upper bound error.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'NegativeOrZeroFloatValueObject value <<<.*>>> must be a negative or zero float.',
    ):
        NegativeOrZeroFloatValueObject(value=FloatMother.positive())


@mark.unit_testing
def test_negative_or_zero_float_value_object_invalid_type() -> None:
    """
    Test NegativeOrZeroFloatValueObject value object raises TypeError when value is not float.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'FloatValueObject value <<<.*>>> must be a float. Got <<<.*>>> type.',
    ):
        NegativeOrZeroFloatValueObject(value=FloatMother.invalid_type())
