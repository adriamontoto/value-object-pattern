"""
Test PositiveOrZeroNumberValueObject value object.
"""

from typing import Any

from object_mother_pattern import FloatMother, IntegerMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables import PositiveOrZeroNumberValueObject


@mark.unit_testing
def test_positive_or_zero_number_value_object_normalizes_integer_to_float() -> None:
    """
    Test PositiveOrZeroNumberValueObject accepts a positive integer and stores a float.
    """
    value = IntegerMother.positive()

    number = PositiveOrZeroNumberValueObject(value=value)

    assert type(number.value) is float
    assert number.value > 0.0


@mark.unit_testing
def test_positive_or_zero_number_value_object_accepts_positive_float() -> None:
    """
    Test PositiveOrZeroNumberValueObject preserves a positive float.
    """
    value = FloatMother.positive()

    number = PositiveOrZeroNumberValueObject(value=value)

    assert type(number.value) is float
    assert number.value > 0.0


@mark.unit_testing
def test_positive_or_zero_number_value_object_accepts_zero_boundary() -> None:
    """
    Test PositiveOrZeroNumberValueObject accepts integer and negative floating-point zero.
    """
    values = (IntegerMother.create(value=0), FloatMother.create(value=-0.0))

    for value in values:
        number = PositiveOrZeroNumberValueObject(value=value)

        assert type(number.value) is float
        assert number.value == 0.0
        assert str(number.value) == '0.0'


@mark.unit_testing
def test_positive_or_zero_number_value_object_rejects_negative_values() -> None:
    """
    Test PositiveOrZeroNumberValueObject rejects negative integers and floats.
    """
    values = (IntegerMother.negative(), FloatMother.negative())

    for value in values:
        with assert_raises(
            expected_exception=ValueError,
            match=(rf'PositiveOrZeroNumberValueObject value <<<{value}>>> must be greater than or equal to zero.'),
        ):
            PositiveOrZeroNumberValueObject(value=value)


@mark.unit_testing
def test_positive_or_zero_number_value_object_rejects_invalid_type() -> None:
    """
    Test PositiveOrZeroNumberValueObject rejects values other than exact integers and floats.
    """
    value: Any = FloatMother.invalid_type()

    with assert_raises(
        expected_exception=TypeError,
        match=r'NumberValueObject value <<<.*>>> must be an integer or float. Got <<<.*>>> type.',
    ):
        PositiveOrZeroNumberValueObject(value=value)
