"""
Test TrueValueObject value object.
"""

from object_mother_pattern.mothers import BooleanMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.primitives import TrueValueObject


@mark.unit_testing
def test_true_value_object_happy_path() -> None:
    """
    Test TrueValueObject value object happy path.
    """
    boolean_value = TrueValueObject(value=BooleanMother.true())

    assert type(boolean_value.value) is bool
    assert boolean_value.value


@mark.unit_testing
def test_true_value_object_invalid_value() -> None:
    """
    Test TrueValueObject value object raises ValueError when value is not True.
    """
    with assert_raises(
        expected_exception=ValueError,
        match='TrueValueObject value <<<False>>> must be true.',
    ):
        TrueValueObject(value=BooleanMother.false())


@mark.unit_testing
def test_true_value_object_invalid_type() -> None:
    """
    Test TrueValueObject value object raises TypeError when value is not boolean.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'TrueValueObject value <<<.*>>> must be a boolean. Got <<<.*>>> type.',
    ):
        TrueValueObject(value=BooleanMother.invalid_type())
