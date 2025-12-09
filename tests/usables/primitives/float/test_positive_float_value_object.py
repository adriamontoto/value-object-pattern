"""
Test PositiveFloatValueObject value object.
"""

from object_mother_pattern import FloatMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.primitives.float import PositiveFloatValueObject


@mark.unit_testing
def test_positive_float_value_object_happy_path() -> None:
    """
    Test PositiveFloatValueObject value object happy path.
    """
    value_object = PositiveFloatValueObject(value=FloatMother.positive())

    assert type(value_object.value) is float
    assert value_object.value > 0.0


@mark.unit_testing
def test_positive_float_value_object_lower_bound() -> None:
    """
    Test PositiveFloatValueObject value object lower bound.
    """
    PositiveFloatValueObject(value=FloatMother.create(value=0.000001))


@mark.unit_testing
def test_positive_float_value_object_lower_bound_error() -> None:
    """
    Test PositiveFloatValueObject value object lower bound error.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'PositiveFloatValueObject value <<<.*>>> must be a positive float.',
    ):
        PositiveFloatValueObject(value=FloatMother.create(value=0.0))


@mark.unit_testing
def test_positive_float_value_object_random_lower_bound_error() -> None:
    """
    Test PositiveFloatValueObject value object random lower bound error.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'PositiveFloatValueObject value <<<.*>>> must be a positive float.',
    ):
        PositiveFloatValueObject(value=FloatMother.negative_or_zero())


@mark.unit_testing
def test_positive_float_value_object_invalid_type() -> None:
    """
    Test PositiveFloatValueObject value object raises TypeError when value is not float.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'FloatValueObject value <<<.*>>> must be a float. Got <<<.*>>> type.',
    ):
        PositiveFloatValueObject(value=FloatMother.invalid_type())
