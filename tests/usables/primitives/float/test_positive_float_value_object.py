"""
Test PositiveFloatValueObject value object.
"""

from object_mother_pattern.mothers import FloatMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.primitives import PositiveFloatValueObject


@mark.unit_testing
def test_positive_float_value_object_happy_path() -> None:
    """
    Test PositiveFloatValueObject value object happy path.
    """
    float_value = PositiveFloatValueObject(value=FloatMother.positive())

    assert type(float_value.value) is float
    assert float_value.value > 0


@mark.unit_testing
def test_positive_float_value_object_invalid_value() -> None:
    """
    Test PositiveFloatValueObject value object raises ValueError when value is not positive.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'PositiveFloatValueObject value <<<.*>>> must be a positive float.',
    ):
        PositiveFloatValueObject(value=FloatMother.create(max=0))


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
