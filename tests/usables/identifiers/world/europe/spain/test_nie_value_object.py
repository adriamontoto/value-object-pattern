"""
Test NieValueObject value object.
"""

from typing import Any

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.identifiers.world.europe.spain import NieValueObject


@mark.unit_testing
def test_nie_value_object_happy_path() -> None:
    """
    Test NieValueObject value object happy path.
    """
    nie_value = NieValueObject(value='x-1234567-l')

    assert type(nie_value.value) is str
    assert nie_value.value == 'X1234567L'
    assert NieValueObject.identification_regex().fullmatch('x-1234567-l')
    assert NieValueObject.validation_regex().fullmatch(nie_value.value)


@mark.unit_testing
def test_nie_value_object_invalid_value() -> None:
    """
    Test NieValueObject value object raises ValueError when value is not a Spanish NIE.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'NieValueObject value <<<not-a-nie>>> is not a valid Spanish NIE.',
    ):
        NieValueObject(value='not-a-nie')


@mark.unit_testing
def test_nie_value_object_invalid_control_letter() -> None:
    """
    Test NieValueObject value object raises ValueError when value has an invalid control letter.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'NieValueObject value <<<X1234567T>>> is not a valid Spanish NIE.',
    ):
        NieValueObject(value='X1234567T')


@mark.unit_testing
def test_nie_value_object_invalid_processed_value() -> None:
    """
    Test NieValueObject defensive validation branch for invalid processed values.
    """
    nie_value: Any = NieValueObject(value='x-1234567-l')

    with assert_raises(
        expected_exception=ValueError,
        match=r'NieValueObject value <<<X1234567L>>> is not a valid Spanish NIE.',
    ):
        nie_value._ensure_value_follows_validation_regex(value='X1234567L', processed_value='INVALID')
