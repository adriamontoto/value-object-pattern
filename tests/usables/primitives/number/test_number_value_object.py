"""
Test NumberValueObject value object.
"""

from typing import Any

from object_mother_pattern import BooleanMother, FloatMother, IntegerMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables import NumberValueObject


@mark.unit_testing
def test_number_value_object_normalizes_integer_to_float() -> None:
    """
    Test NumberValueObject accepts an integer and stores a float.
    """
    value = IntegerMother.create(value=-2)

    number = NumberValueObject(value=value)

    assert type(number.value) is float
    assert number.value == -2.0


@mark.unit_testing
def test_number_value_object_accepts_float() -> None:
    """
    Test NumberValueObject preserves a finite float.
    """
    value = FloatMother.create(value=-2.5)

    assert NumberValueObject(value=value).value == value


@mark.unit_testing
def test_number_value_object_normalizes_negative_zero() -> None:
    """
    Test NumberValueObject canonicalizes negative zero as positive zero.
    """
    value = FloatMother.create(value=-0.0)

    number = NumberValueObject(value=value)

    assert number.value == 0.0
    assert str(number.value) == '0.0'


@mark.unit_testing
def test_number_value_object_rejects_invalid_type() -> None:
    """
    Test NumberValueObject rejects values other than exact integers and floats.
    """
    value: Any = FloatMother.invalid_type()

    with assert_raises(
        expected_exception=TypeError,
        match=r'NumberValueObject value <<<.*>>> must be an integer or float. Got <<<.*>>> type.',
    ):
        NumberValueObject(value=value)


@mark.unit_testing
def test_number_value_object_rejects_boolean() -> None:
    """
    Test NumberValueObject rejects bool even though bool subclasses int.
    """
    value: Any = BooleanMother.true()

    with assert_raises(
        expected_exception=TypeError,
        match=r'NumberValueObject value <<<True>>> must be an integer or float. Got <<<bool>>> type.',
    ):
        NumberValueObject(value=value)


@mark.unit_testing
def test_number_value_object_rejects_non_finite_float() -> None:
    """
    Test NumberValueObject rejects NaN and infinities.
    """
    values = (
        FloatMother.create(value=float('nan')),
        FloatMother.create(value=float('inf')),
        FloatMother.create(value=float('-inf')),
    )

    for value in values:
        with assert_raises(
            expected_exception=ValueError,
            match=r'NumberValueObject value <<<.*>>> must be finite and representable as a float.',
        ):
            NumberValueObject(value=value)


@mark.unit_testing
def test_number_value_object_rejects_integer_that_overflows_float() -> None:
    """
    Test NumberValueObject rejects integers too large for a finite float.
    """
    value = IntegerMother.create(value=10**1000)

    with assert_raises(
        expected_exception=ValueError,
        match=r'NumberValueObject value <<<.*>>> must be finite and representable as a float.',
    ):
        NumberValueObject(value=value)
