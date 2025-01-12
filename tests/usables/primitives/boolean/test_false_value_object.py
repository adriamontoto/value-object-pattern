"""
Test FalseValueObject value object.
"""

from object_mother_pattern.mothers import BooleanMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.primitives import FalseValueObject


@mark.unit_testing
def test_false_value_object_happy_path() -> None:
    """
    Test FalseValueObject value object happy path.
    """
    boolean_value = FalseValueObject(value=BooleanMother.create(value=False))

    assert not boolean_value.value


@mark.unit_testing
def test_false_value_object_invalid_value() -> None:
    """
    Test FalseValueObject value object raises ValueError when value is not False.
    """
    with assert_raises(
        expected_exception=ValueError,
        match='FalseValueObject value <<<True>>> must be false.',
    ):
        FalseValueObject(value=BooleanMother.create(value=True))


@mark.unit_testing
def test_false_value_object_invalid_type() -> None:
    """
    Test FalseValueObject value object raises TypeError when value is not boolean.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'BooleanValueObject value <<<.*>>> must be a boolean. Got <<<.*>>> type.',
    ):
        FalseValueObject(value=BooleanMother.invalid_type())
