"""
Test PassportValueObject value object.
"""

from typing import Any

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.identifiers.world.europe.spain import PassportValueObject


@mark.unit_testing
def test_passport_value_object_happy_path() -> None:
    """
    Test PassportValueObject value object happy path.
    """
    passport_value = PassportValueObject(value='abc123456')

    assert type(passport_value.value) is str
    assert passport_value.value == 'ABC123456'
    assert PassportValueObject.identification_regex().fullmatch('abc123456')
    assert PassportValueObject.validation_regex().fullmatch(passport_value.value)


@mark.unit_testing
def test_passport_value_object_invalid_value() -> None:
    """
    Test PassportValueObject value object raises ValueError when value is not a Spanish passport.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'PassportValueObject value <<<A12345678>>> is not a valid Spanish passport.',
    ):
        PassportValueObject(value='A12345678')


@mark.unit_testing
def test_passport_value_object_invalid_processed_value() -> None:
    """
    Test PassportValueObject defensive validation branch for invalid processed values.
    """
    passport_value: Any = PassportValueObject(value='abc123456')

    with assert_raises(
        expected_exception=ValueError,
        match=r'PassportValueObject value <<<ABC123456>>> is not a valid Spanish passport.',
    ):
        passport_value._ensure_value_follows_validation_regex(value='ABC123456', processed_value='INVALID')
