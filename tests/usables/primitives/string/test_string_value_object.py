"""
Test StringValueObject value object.
"""

from object_mother_pattern import StringMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables import StringValueObject


@mark.unit_testing
def test_string_value_object_happy_path() -> None:
    """
    Test StringValueObject value object happy path.
    """
    string_value = StringValueObject(value=StringMother.create())

    assert type(string_value.value) is str


@mark.unit_testing
def test_string_value_object_invalid_type() -> None:
    """
    Test StringValueObject value object raises TypeError when value is not string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'StringValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        StringValueObject(value=StringMother.invalid_type())
