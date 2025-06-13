"""
Test FloatValueObject value object.
"""

from object_mother_pattern.mothers import FloatMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables import FloatValueObject


@mark.unit_testing
def test_float_value_object_happy_path() -> None:
    """
    Test FloatValueObject value object happy path.
    """
    float_value = FloatValueObject(value=FloatMother.create())

    assert type(float_value.value) is float


@mark.unit_testing
def test_float_value_object_invalid_type() -> None:
    """
    Test FloatValueObject value object raises TypeError when value is not float.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'FloatValueObject value <<<.*>>> must be a float. Got <<<.*>>> type.',
    ):
        FloatValueObject(value=FloatMother.invalid_type())
