"""
Test process decorator.
"""

from object_mother_pattern.mothers import IntegerMother
from pytest import mark, raises as assert_raises

from value_object_pattern.decorators import process


@mark.unit_testing
def test_process_uses_function_name_when_order_is_provided() -> None:
    """
    Test that process decorator uses the provided order when order is provided.
    """
    order = IntegerMother.positive()

    @process(order=order)
    def ensure_something(value: str) -> None:  # pragma: no cover
        pass

    assert ensure_something._order == str(order)  # type: ignore[attr-defined]


@mark.unit_testing
def test_process_uses_function_name_when_order_not_provided() -> None:
    """
    Test that process decorator falls back to the function name when order is not provided.
    """

    @process()
    def ensure_something(value: str) -> None:  # pragma: no cover
        pass

    assert ensure_something._order == 'ensure_something'  # type: ignore[attr-defined]


@mark.unit_testing
def test_process_raises_type_error_when_order_is_not_integer() -> None:
    """
    Test that process decorator raises TypeError when order is not an integer.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'Process order <<<.*>>> must be an integer\. Got <<<.*>>> type\.',
    ):

        @process(order=IntegerMother.invalid_type())
        def _(_: str) -> None:  # pragma: no cover
            pass


@mark.unit_testing
def test_process_raises_value_error_when_order_is_negative() -> None:
    """
    Test that process decorator raises ValueError when order is negative.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'Process order <<<-1>>> must be equal or greater than 0\.',
    ):

        @process(order=-1)
        def _(_: str) -> None:  # pragma: no cover
            pass


@mark.unit_testing
def test_process_raises_value_error_when_order_is_negative_random() -> None:
    """
    Test that process decorator raises ValueError when order is negative random.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'Process order <<<.*>>> must be equal or greater than 0\.',
    ):

        @process(order=IntegerMother.negative())
        def _(_: str) -> None:  # pragma: no cover
            pass
