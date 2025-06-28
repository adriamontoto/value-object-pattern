"""
Test PrintableStringValueObject value object.
"""

from object_mother_pattern import StringMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables import PrintableStringValueObject


@mark.unit_testing
def test_printable_string_value_object_happy_path() -> None:
    """
    Test PrintableStringValueObject value object happy path.
    """
    string_value = PrintableStringValueObject(value=StringMother.create())

    assert type(string_value.value) is str
    assert string_value.value.isprintable()


@mark.unit_testing
def test_printable_string_value_object_invalid_value() -> None:
    """
    Test PrintableStringValueObject value object raises ValueError when value contains not printable characters.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'PrintableStringValueObject value <<<.*>>> contains invalid characters. Only printable characters are allowed.',  # noqa: E501
    ):
        PrintableStringValueObject(value=StringMother.invalid_value())


@mark.unit_testing
def test_printable_string_value_object_invalid_type() -> None:
    """
    Test PrintableStringValueObject value object raises TypeError when value is not string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'StringValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        PrintableStringValueObject(value=StringMother.invalid_type())
