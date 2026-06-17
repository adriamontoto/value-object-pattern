"""
Test AmexCreditCardValueObject value object.
"""

from typing import Any

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.money.credit_cards import AmexCreditCardValueObject


@mark.unit_testing
def test_amex_credit_card_value_object_happy_path() -> None:
    """
    Test AmexCreditCardValueObject value object happy path.
    """
    raw_value = '3714-496353-98431'
    expected_value = '371449635398431'

    card = AmexCreditCardValueObject(value=raw_value)

    assert type(card.value) is str
    assert card.value == expected_value
    assert AmexCreditCardValueObject.identification_regex().fullmatch(raw_value)
    assert AmexCreditCardValueObject.validation_regex().fullmatch(expected_value)


@mark.unit_testing
def test_amex_credit_card_value_object_invalid_value() -> None:
    """
    Test AmexCreditCardValueObject value object raises ValueError when value is not an Amex card.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'AmexCreditCardValueObject value <<<4111111111111111>>> is not a valid American Express credit card number.',  # noqa: E501
    ):
        AmexCreditCardValueObject(value='4111111111111111')


@mark.unit_testing
def test_amex_credit_card_value_object_invalid_luhn_checksum() -> None:
    """
    Test AmexCreditCardValueObject value object raises ValueError when value has an invalid Luhn checksum.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'AmexCreditCardValueObject value <<<371449635398432>>> is not a valid American Express credit card number.',  # noqa: E501
    ):
        AmexCreditCardValueObject(value='371449635398432')


@mark.unit_testing
def test_amex_credit_card_value_object_invalid_processed_value() -> None:
    """
    Test AmexCreditCardValueObject defensive validation branch for invalid processed values.
    """
    card: Any = AmexCreditCardValueObject(value='3714-496353-98431')

    with assert_raises(
        expected_exception=ValueError,
        match=r'AmexCreditCardValueObject value <<<371449635398431>>> is not a valid American Express credit card number.',  # noqa: E501
    ):
        card._ensure_value_follows_validation_regex(value='371449635398431', processed_value='INVALID')
