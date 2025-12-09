"""
Test enumeration value object module.
"""

from enum import Enum

from object_mother_pattern.models import EnumerationMother
from object_mother_pattern.mothers import StringMother
from pytest import mark, raises as assert_raises

from value_object_pattern import EnumerationValueObject


class Color(Enum):
    """
    Enumeration used for tests.
    """

    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'


class ColorValueObject(EnumerationValueObject[Color]):
    """
    Enumeration value object for Color enumeration.
    """


class ColorMother(EnumerationMother[Color]):
    """
    Object mother for Color enumeration.
    """


@mark.unit_testing
def test_enumeration_value_object_accepts_enum_member() -> None:
    """
    Test that the value object accepts enumeration members directly.
    """
    color = ColorMother.create()
    value_object = ColorValueObject(value=color)

    assert value_object.value is color


@mark.unit_testing
def test_enumeration_value_object_processes_raw_value_to_enum() -> None:
    """
    Test that the value object converts raw enumeration values to enumeration members.
    """
    color = ColorMother.create().value
    value_object = ColorValueObject(value=color)

    assert value_object.value.value is color


@mark.unit_testing
def test_enumeration_value_object_processes_raw_name_to_enum() -> None:
    """
    Test that the value object converts raw enumeration names to enumeration members and raises TypeError for invalid
    types.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'ColorValueObject value <<<.*>>> must be from the enumeration <<<Color>>>. Got <<<.*>>> type\.',
    ):
        ColorValueObject(value=ColorMother.create().name)


@mark.unit_testing
def test_enumeration_value_object_raises_type_error_for_invalid_value() -> None:
    """
    Test that the value object raises a TypeError when the value is not part of the enumeration.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'ColorValueObject value <<<.*>>> must be from the enumeration <<<Color>>>. Got <<<.*>>> type\.',
    ):
        ColorValueObject(value=StringMother.create())


@mark.unit_testing
def test_enumeration_value_object_raises_type_error_for_invalid_type() -> None:
    """
    Test that the value object raises a TypeError when the value is of an invalid type.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'ColorValueObject value <<<.*>>> must be from the enumeration <<<Color>>>. Got <<<.*>>> type\.',
    ):
        ColorValueObject(value=ColorMother.invalid_type())


@mark.unit_testing
def test_enumeration_value_object_requires_parameterization() -> None:
    """
    Test that __init_subclass__ raises a TypeError when the class is not parameterized.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'EnumerationValueObject must be parameterized, e\.g\. "class ColorValueObject\(EnumerationValueObject\[ColorEnumeration\]\)".',  # noqa: E501
    ):

        class _InvalidEnumerationValueObject(EnumerationValueObject):  # type: ignore[type-arg]  # pragma: no cover
            pass


@mark.unit_testing
def test_enumeration_value_object_requires_enum_subclass() -> None:
    """
    Test that __init_subclass__ raises a TypeError when the generic argument is not an Enum subclass.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r"EnumerationValueObject\[\.\.\.\] <<<<class 'int'>>>> must be an Enum subclass\. Got <<<type>>> type\.",
    ):

        class _InvalidTypeEnumerationValueObject(EnumerationValueObject[int]):  # type: ignore[type-var]  # pragma: no cover
            pass
