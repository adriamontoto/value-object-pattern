"""
Test value object validate method.
"""

from re import escape

from object_mother_pattern.mothers import IntegerMother
from pytest import mark, raises as assert_raises

from value_object_pattern import ValueObject, validation


class NaturalValueObject(ValueObject[int]):
    """
    NaturalValueObject value object class.
    """

    @validation(order=0)
    def ensure_value_is_integer(self, value: int) -> None:
        """
        Ensures the value object is an integer.

        Args:
            value (int): Value object.

        Raises:
            TypeError: If the value object is not an integer.
        """
        if type(value) is not int:
            raise TypeError(f'Value object must be an integer, not {type(value).__name__}.')

    @validation(order=1)
    def ensure_value_is_positive(self, value: int) -> None:
        """
        Ensures the value object is a positive number, including zero.

        Args:
            value (int): Value object.

        Raises:
            ValueError: If the value object is not a natural number.
        """
        if value < 0:
            raise ValueError('Value object must be a positive number.')

    @validation()
    def ensure_value_is_not_zero(self, value: int) -> None:
        """
        Ensures the value object is not zero.

        Args:
            value (int): Value object.

        Raises:
            ValueError: If the value object is zero.
        """
        if value == 0:
            raise ValueError('Value object must not be zero.')


@mark.unit_testing
def test_value_object_validate_method_happy_path() -> None:
    """
    Test value object validate method happy path, no validation errors.
    """
    natural_value = IntegerMother.positive()
    NaturalValueObject(value=natural_value)


@mark.unit_testing
def test_value_object_validate_method_invalid_type() -> None:
    """
    Test value object validate method invalid type.
    """
    invalid_natural = IntegerMother.invalid_type()

    with assert_raises(
        expected_exception=TypeError,
        match=f'Value object must be an integer, not {type(invalid_natural).__name__}.',
    ):
        NaturalValueObject(value=invalid_natural)


@mark.unit_testing
def test_value_object_validate_method_invalid_value() -> None:
    """
    Test value object validate method invalid value.
    """
    invalid_natural = IntegerMother.create(min=-100, max=-1)

    with assert_raises(
        expected_exception=ValueError,
        match='Value object must be a positive number.',
    ):
        NaturalValueObject(value=invalid_natural)


@mark.unit_testing
def test_value_object_validate_method_is_zero() -> None:
    """
    Test value object validate method is zero.
    """
    zero = IntegerMother.create(value=0)

    with assert_raises(
        expected_exception=ValueError,
        match='Value object must not be zero.',
    ):
        NaturalValueObject(value=zero)


@mark.unit_testing
def test_value_object_validation_method_order_happy_path() -> None:
    """
    Test value object validation method invalid type.
    """

    class UpperStringValueObject(ValueObject[str]):
        @validation(order=IntegerMother.create(min=0))
        def ensure_value_is_integer(self, value: int) -> None:
            if type(value) is not int:
                raise TypeError(f'Value object must be an integer, not {type(value).__name__}.')


@mark.unit_testing
def test_value_object_validation_method_order_invalid_type() -> None:
    """
    Test value object validation method invalid type.
    """
    invalid_integer = IntegerMother.invalid_type()

    with assert_raises(
        expected_exception=TypeError,
        match=f'Validation order <<<{escape(pattern=str(invalid_integer))}>>> must be an integer. Got <<<{type(invalid_integer).__name__}>>> type.',  # noqa: E501
    ):

        class NaturalValueObject(ValueObject[int]):
            @validation(order=invalid_integer)
            def ensure_value_is_integer(self, value: int) -> None:
                if type(value) is not int:
                    raise TypeError(f'Value object must be an integer, not {type(value).__name__}.')


@mark.unit_testing
def test_value_object_validation_method_order_invalid_value() -> None:
    """
    Test value object validation method invalid value.
    """
    invalid_integer = IntegerMother.negative()

    with assert_raises(
        expected_exception=ValueError,
        match=f'Validation order <<<{invalid_integer}>>> must be equal or greater than 0.',
    ):

        class NaturalValueObject(ValueObject[int]):
            @validation(order=invalid_integer)
            def ensure_value_is_integer(self, value: int) -> None:
                if type(value) is not int:
                    raise TypeError(f'Value object must be an integer, not {type(value).__name__}.')
