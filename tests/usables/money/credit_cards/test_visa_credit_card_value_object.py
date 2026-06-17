"""
Test VisaCreditCardValueObject value object.
"""

from typing import Any

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.money.credit_cards import VisaCreditCardValueObject


@mark.unit_testing
def test_visa_credit_card_value_object_happy_path() -> None:
    """
    Test VisaCreditCardValueObject value object happy path.
    """
    raw_value = '4111-1111-1111-1111'
    expected_value = '4111111111111111'

    card = VisaCreditCardValueObject(value=raw_value)

    assert type(card.value) is str
    assert card.value == expected_value
    assert VisaCreditCardValueObject.identification_regex().fullmatch(raw_value)
    assert VisaCreditCardValueObject.validation_regex().fullmatch(expected_value)


@mark.unit_testing
def test_visa_credit_card_value_object_invalid_value() -> None:
    """
    Test VisaCreditCardValueObject value object raises ValueError when value is not a Visa card.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'VisaCreditCardValueObject value <<<5555555555554444>>> is not a valid Visa credit card number.',
    ):
        VisaCreditCardValueObject(value='5555555555554444')


@mark.unit_testing
def test_visa_credit_card_value_object_invalid_luhn_checksum() -> None:
    """
    Test VisaCreditCardValueObject value object raises ValueError when value has an invalid Luhn checksum.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'VisaCreditCardValueObject value <<<4111111111111112>>> is not a valid Visa credit card number.',
    ):
        VisaCreditCardValueObject(value='4111111111111112')


@mark.unit_testing
def test_visa_credit_card_value_object_invalid_processed_value() -> None:
    """
    Test VisaCreditCardValueObject defensive validation branch for invalid processed values.
    """
    card: Any = VisaCreditCardValueObject(value='4111-1111-1111-1111')

    with assert_raises(
        expected_exception=ValueError,
        match=r'VisaCreditCardValueObject value <<<4111111111111111>>> is not a valid Visa credit card number.',
    ):
        card._ensure_value_follows_validation_regex(value='4111111111111111', processed_value='INVALID')
