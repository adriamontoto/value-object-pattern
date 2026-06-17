"""
Test NifValueObject value object.
"""

from typing import Any

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.identifiers.world.europe.spain import NifValueObject

_NIF_LETTER_CONTROL_LETTERS = ['J', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']


def _calculate_nif_control_values(*, number: str) -> tuple[str, str]:
    """
    Calculate Spanish NIF control values for tests.
    """
    total = 0
    for index, digit in enumerate(iterable=number):
        value = int(digit)
        if index % 2 == 0:
            value *= 2
            if value >= 10:
                value = value // 10 + value % 10

        total += value

    control_value = (10 - (total % 10)) % 10

    return str(control_value), _NIF_LETTER_CONTROL_LETTERS[control_value]


def _nif_value(*, prefix: str, number: str, control_kind: str) -> str:
    """
    Build a valid Spanish NIF from its prefix, number, and expected control kind.
    """
    expected_number, expected_letter = _calculate_nif_control_values(number=number)
    control = expected_number if control_kind == 'number' else expected_letter

    return f'{prefix}{number}{control}'


@mark.unit_testing
def test_nif_value_object_digit_control_happy_path() -> None:
    """
    Test NifValueObject value object accepts digit control NIF values.
    """
    nif_value = NifValueObject(value='a-5881850-1')

    assert type(nif_value.value) is str
    assert nif_value.value == 'A58818501'
    assert NifValueObject.identification_regex().fullmatch('a-5881850-1')
    assert NifValueObject.validation_regex().fullmatch(nif_value.value)


@mark.unit_testing
def test_nif_value_object_letter_control_happy_path() -> None:
    """
    Test NifValueObject value object accepts letter control NIF values.
    """
    nif_value = NifValueObject(value=_nif_value(prefix='P', number='1234567', control_kind='letter'))

    assert nif_value.value.startswith('P1234567')


@mark.unit_testing
def test_nif_value_object_mixed_control_happy_path() -> None:
    """
    Test NifValueObject value object accepts mixed control NIF values.
    """
    nif_value = NifValueObject(value=_nif_value(prefix='V', number='1234567', control_kind='number'))

    assert nif_value.value.startswith('V1234567')


@mark.unit_testing
def test_nif_value_object_invalid_value() -> None:
    """
    Test NifValueObject value object raises ValueError when value is not a Spanish company NIF.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'NifValueObject value <<<not-a-nif>>> is not a valid Spanish company NIF.',
    ):
        NifValueObject(value='not-a-nif')


@mark.unit_testing
def test_nif_value_object_invalid_control_character() -> None:
    """
    Test NifValueObject value object raises ValueError when value has an invalid control character.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'NifValueObject value <<<A58818502>>> is not a valid Spanish company NIF.',
    ):
        NifValueObject(value='A58818502')


@mark.unit_testing
def test_nif_value_object_invalid_processed_value() -> None:
    """
    Test NifValueObject defensive validation branch for invalid processed values.
    """
    nif_value: Any = NifValueObject(value='a-5881850-1')

    with assert_raises(
        expected_exception=ValueError,
        match=r'NifValueObject value <<<A58818501>>> is not a valid Spanish company NIF.',
    ):
        nif_value._ensure_value_follows_validation_regex(value='A58818501', processed_value='INVALID')
