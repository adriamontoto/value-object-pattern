"""
Test PositiveOrZeroFloatValueObject value object.
"""

from object_mother_pattern import FloatMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.primitives.float import PositiveOrZeroFloatValueObject


@mark.unit_testing
def test_positive_or_zero_float_value_object_happy_path() -> None:
    """
    Test PositiveOrZeroFloatValueObject value object happy path.
    """
    value_object = PositiveOrZeroFloatValueObject(value=FloatMother.positive_or_zero())

    assert type(value_object.value) is float
    assert value_object.value >= 0.0


@mark.unit_testing
def test_positive_or_zero_float_value_object_lower_bound() -> None:
    """
    Test PositiveOrZeroFloatValueObject value object lower bound.
    """
    PositiveOrZeroFloatValueObject(value=FloatMother.create(value=0.0))


@mark.unit_testing
def test_positive_or_zero_float_value_object_lower_bound_error() -> None:
    """
    Test PositiveOrZeroFloatValueObject value object lower bound error.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'PositiveOrZeroFloatValueObject value <<<.*>>> must be a positive or zero float.',
    ):
        PositiveOrZeroFloatValueObject(value=FloatMother.create(value=-0.000001))


@mark.unit_testing
def test_positive_or_zero_float_value_object_random_lower_bound_error() -> None:
    """
    Test PositiveOrZeroFloatValueObject value object random lower bound error.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'PositiveOrZeroFloatValueObject value <<<.*>>> must be a positive or zero float.',
    ):
        PositiveOrZeroFloatValueObject(value=FloatMother.negative())


@mark.unit_testing
def test_positive_or_zero_float_value_object_invalid_type() -> None:
    """
    Test PositiveOrZeroFloatValueObject value object raises TypeError when value is not float.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'FloatValueObject value <<<.*>>> must be a float. Got <<<.*>>> type.',
    ):
        PositiveOrZeroFloatValueObject(value=FloatMother.invalid_type())
