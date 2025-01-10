"""
Test BooleanValueObject value object.
"""

from object_mother_pattern.mothers import BooleanMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.primitives import BooleanValueObject


@mark.unit_testing
def test_boolean_value_object_happy_path() -> None:
    """
    Test BooleanValueObject value object happy path.
    """
    boolean_value = BooleanValueObject(value=BooleanMother.create())

    assert type(boolean_value.value) is bool


@mark.unit_testing
def test_boolean_value_object_invalid_type() -> None:
    """
    Test BooleanValueObject value object raises TypeError when value is not boolean.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'BooleanValueObject value <<<.*>>> must be a boolean. Got <<<.*>>> type.',
    ):
        BooleanValueObject(value=BooleanMother.invalid_type())
