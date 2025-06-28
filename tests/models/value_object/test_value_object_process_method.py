"""
Test value object process method.
"""

from object_mother_pattern import IntegerMother
from pytest import mark, raises as assert_raises

from value_object_pattern import ValueObject, process


@mark.unit_testing
def test_value_object_process_method_order_happy_path() -> None:
    """
    Test value object process method invalid type.
    """

    class UpperStringValueObject(ValueObject[str]):
        @process(order=IntegerMother.create(min=0))
        def ensure_value_is_upper(self, value: str) -> str:
            return value.upper()


@mark.unit_testing
def test_value_object_process_method_order_invalid_type() -> None:
    """
    Test value object process method invalid type.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'Process order <<<.*>>> must be an integer. Got <<<.*>>> type.',
    ):

        class UpperStringValueObject(ValueObject[str]):
            @process(order=IntegerMother.invalid_type())
            def ensure_value_is_upper(self, value: str) -> str:
                return value.upper()


@mark.unit_testing
def test_value_object_process_method_order_invalid_value() -> None:
    """
    Test value object process method invalid value.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'Process order <<<.*>>> must be equal or greater than 0.',
    ):

        class UpperStringValueObject(ValueObject[str]):
            @process(order=IntegerMother.negative())
            def ensure_value_is_upper(self, value: str) -> str:
                return value.upper()
