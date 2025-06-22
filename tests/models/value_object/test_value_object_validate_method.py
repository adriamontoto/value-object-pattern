"""
Test value object validate method.
"""

from object_mother_pattern import IntegerMother
from pytest import mark, raises as assert_raises

from value_object_pattern import ValueObject, validation


@mark.unit_testing
def test_value_object_validation_method_order_happy_path() -> None:
    """
    Test value object validation method invalid type.
    """

    class PositiveIntegerValueObject(ValueObject[int]):
        @validation()
        def ensure_value_is_integer(self, value: int) -> None:
            if type(value) is not int:
                raise TypeError(f'Value object must be an integer, not {type(value).__name__}.')


@mark.unit_testing
def test_value_object_validation_method_order_invalid_type() -> None:
    """
    Test value object validation method invalid type.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'Validation order <<<.*>>> must be an integer. Got <<<.*>>> type.',
    ):

        class PositiveIntegerValueObject(ValueObject[int]):
            @validation(order=IntegerMother.invalid_type())
            def ensure_value_is_integer(self, value: int) -> None:
                if type(value) is not int:
                    raise TypeError(f'Value object must be an integer, not {type(value).__name__}.')


@mark.unit_testing
def test_value_object_validation_method_order_invalid_value() -> None:
    """
    Test value object validation method invalid value.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'Validation order <<<.*>>> must be equal or greater than 0.',
    ):

        class PositiveIntegerValueObject(ValueObject[int]):
            @validation(order=IntegerMother.negative())
            def ensure_value_is_integer(self, value: int) -> None:
                if type(value) is not int:
                    raise TypeError(f'Value object must be an integer, not {type(value).__name__}.')
