"""
Test validation decorator.
"""

from object_mother_pattern.mothers import BooleanMother, IntegerMother
from pytest import mark, raises as assert_raises

from value_object_pattern.decorators import validation


@mark.unit_testing
def test_validation_uses_function_name_when_order_is_provided() -> None:
    """
    Test that validation decorator uses the provided order when order is provided.
    """
    order = IntegerMother.positive()

    @validation(order=order)
    def ensure_something(value: str) -> None:  # pragma: no cover
        pass

    assert ensure_something._order == str(order)  # type: ignore[attr-defined]


@mark.unit_testing
def test_validation_uses_function_name_when_order_not_provided() -> None:
    """
    Test that validation decorator falls back to the function name when order is not provided.
    """

    @validation()
    def ensure_something(value: str) -> None:  # pragma: no cover
        pass

    assert ensure_something._order == 'ensure_something'  # type: ignore[attr-defined]


@mark.unit_testing
def test_validation_uses_function_name_when_early_process_is_provided() -> None:
    """
    Test that validation decorator falls back to the function name when early_process is provided.
    """
    early_process = BooleanMother.create()

    @validation(early_process=early_process)
    def ensure_something(value: str) -> None:  # pragma: no cover
        pass

    assert ensure_something._early_process is early_process  # type: ignore[attr-defined]


@mark.unit_testing
def test_validation_uses_function_name_when_early_process_not_provided() -> None:
    """
    Test that validation decorator falls back to the function name when early_process is not provided.
    """

    @validation()
    def ensure_something(value: str) -> None:  # pragma: no cover
        pass

    assert ensure_something._early_process is False  # type: ignore[attr-defined]


@mark.unit_testing
def test_validation_raises_type_error_when_order_is_not_integer() -> None:
    """
    Test that validation decorator raises TypeError when order is not an integer.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'Validation order <<<.*>>> must be an integer\. Got <<<.*>>> type\.',
    ):

        @validation(order=IntegerMother.invalid_type())
        def _(_: str) -> None:  # pragma: no cover
            pass


@mark.unit_testing
def test_validation_raises_value_error_when_order_is_negative() -> None:
    """
    Test that validation decorator raises ValueError when order is negative.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'Validation order <<<-1>>> must be equal or greater than 0\.',
    ):

        @validation(order=-1)
        def _(_: str) -> None:  # pragma: no cover
            pass


@mark.unit_testing
def test_validation_raises_value_error_when_order_is_negative_random() -> None:
    """
    Test that validation decorator raises ValueError when order is negative random.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'Validation order <<<.*>>> must be equal or greater than 0\.',
    ):

        @validation(order=IntegerMother.negative())
        def _(_: str) -> None:  # pragma: no cover
            pass


@mark.unit_testing
def test_validation_raises_type_error_when_early_process_is_not_boolean() -> None:
    """
    Test that validation decorator raises TypeError when early_process is not a boolean.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'Validation early_process <<<.*>>> must be a boolean\. Got <<<.*>>> type\.',
    ):

        @validation(early_process=BooleanMother.invalid_type())
        def _(_: str) -> None:  # pragma: no cover
            pass
