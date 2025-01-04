"""
Test value object process method.
"""

from re import escape

from object_mother_pattern.mothers import IntegerMother, StringMother
from pytest import mark, raises as assert_raises

from value_object_pattern import ValueObject, process


class UpperStringValueObject(ValueObject[str]):
    """
    UpperStringValueObject value object class.
    """

    @process(order=0)
    def aensure_value_is_upper(self, value: str) -> str:
        """
        Ensure the value object is upper case.

        Args:
            value (str): The value object value.

        Returns:
            str: The upper case value object value.
        """
        return value.upper()

    @process(order=1)
    def ensure_value_has_final_a(self, value: str) -> str:
        """
        Ensure the value object has a final 'a'.

        Args:
            value (str): The value object value.

        Returns:
            str: The value object value with a final 'a'.
        """
        return value + 'a'

    @process()
    def aensure_value_has_final_dot(self, value: str) -> str:
        """
        Ensure the value object has a final dot.

        Args:
            value (str): The value object value.

        Returns:
            str: The value object value with a final dot.
        """
        return value + '.'

    @process()
    def zensure_value_has_final_exclamation_mark(self, value: str) -> str:
        """
        Ensure the value object has a final exclamation mark.

        Args:
            value (str): The value object value.

        Returns:
            str: The value object value with a final exclamation mark.
        """
        return value + '!'


@mark.unit_testing
def test_value_object_process_method_happy_path() -> None:
    """
    Test value object process method happy path, no validation errors.
    """
    string_value = StringMother.create().upper()
    string = UpperStringValueObject(value=string_value)

    assert string.value[:-3].isupper()


@mark.unit_testing
def test_value_object_process_method_multiple_decorators() -> None:
    """
    Test value object process method multiple decorators and it follow the order, first the ordered decorators and then
    the unordered decorators following alphabetical order.
    """
    string_value = StringMother.create()
    string = UpperStringValueObject(value=string_value)

    assert string.value[:-3].isupper()
    assert string.value.endswith('a.!')


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
    invalid_integer = IntegerMother.invalid_type()

    with assert_raises(
        expected_exception=TypeError,
        match=f'Process order <<<{escape(pattern=str(invalid_integer))}>>> must be an integer. Got <<<{type(invalid_integer).__name__}>>> type.',  # noqa: E501
    ):

        class UpperStringValueObject(ValueObject[str]):
            @process(order=invalid_integer)
            def ensure_value_is_upper(self, value: str) -> str:
                return value.upper()


@mark.unit_testing
def test_value_object_process_method_order_invalid_value() -> None:
    """
    Test value object process method invalid value.
    """
    invalid_integer = IntegerMother.negative()

    with assert_raises(
        expected_exception=ValueError,
        match=f'Process order <<<{invalid_integer}>>> must be equal or greater than 0.',
    ):

        class UpperStringValueObject(ValueObject[str]):
            @process(order=invalid_integer)
            def ensure_value_is_upper(self, value: str) -> str:
                return value.upper()
