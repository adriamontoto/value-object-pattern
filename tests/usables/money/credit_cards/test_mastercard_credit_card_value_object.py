"""
Test MastercardCreditCardValueObject value object.
"""

from typing import Any

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.money.credit_cards import MastercardCreditCardValueObject


@mark.unit_testing
def test_mastercard_credit_card_value_object_happy_path() -> None:
    """
    Test MastercardCreditCardValueObject value object happy path.
    """
    raw_value = '5555-5555-5555-4444'
    expected_value = '5555555555554444'

    card = MastercardCreditCardValueObject(value=raw_value)

    assert type(card.value) is str
    assert card.value == expected_value
    assert MastercardCreditCardValueObject.identification_regex().fullmatch(raw_value)
    assert MastercardCreditCardValueObject.validation_regex().fullmatch(expected_value)


@mark.unit_testing
def test_mastercard_credit_card_value_object_invalid_value() -> None:
    """
    Test MastercardCreditCardValueObject value object raises ValueError when value is not a Mastercard card.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'MastercardCreditCardValueObject value <<<4111111111111111>>> is not a valid Mastercard credit card number.',  # noqa: E501
    ):
        MastercardCreditCardValueObject(value='4111111111111111')


@mark.unit_testing
def test_mastercard_credit_card_value_object_invalid_luhn_checksum() -> None:
    """
    Test MastercardCreditCardValueObject value object raises ValueError when value has an invalid Luhn checksum.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'MastercardCreditCardValueObject value <<<5555555555554445>>> is not a valid Mastercard credit card number.',  # noqa: E501
    ):
        MastercardCreditCardValueObject(value='5555555555554445')


@mark.unit_testing
def test_mastercard_credit_card_value_object_invalid_processed_value() -> None:
    """
    Test MastercardCreditCardValueObject defensive validation branch for invalid processed values.
    """
    card: Any = MastercardCreditCardValueObject(value='5555-5555-5555-4444')

    with assert_raises(
        expected_exception=ValueError,
        match=r'MastercardCreditCardValueObject value <<<5555555555554444>>> is not a valid Mastercard credit card number.',  # noqa: E501
    ):
        card._ensure_value_follows_validation_regex(value='5555555555554444', processed_value='INVALID')
