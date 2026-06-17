"""
Test DiscoverCreditCardValueObject value object.
"""

from typing import Any

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.money.credit_cards import DiscoverCreditCardValueObject


@mark.unit_testing
def test_discover_credit_card_value_object_happy_path() -> None:
    """
    Test DiscoverCreditCardValueObject value object happy path.
    """
    raw_value = '6011-1111-1111-1117'
    expected_value = '6011111111111117'

    card = DiscoverCreditCardValueObject(value=raw_value)

    assert type(card.value) is str
    assert card.value == expected_value
    assert DiscoverCreditCardValueObject.identification_regex().fullmatch(raw_value)
    assert DiscoverCreditCardValueObject.validation_regex().fullmatch(expected_value)


@mark.unit_testing
def test_discover_credit_card_value_object_invalid_value() -> None:
    """
    Test DiscoverCreditCardValueObject value object raises ValueError when value is not a Discover card.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'DiscoverCreditCardValueObject value <<<4111111111111111>>> is not a valid Discover credit card number.',  # noqa: E501
    ):
        DiscoverCreditCardValueObject(value='4111111111111111')


@mark.unit_testing
def test_discover_credit_card_value_object_invalid_luhn_checksum() -> None:
    """
    Test DiscoverCreditCardValueObject value object raises ValueError when value has an invalid Luhn checksum.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'DiscoverCreditCardValueObject value <<<6011111111111118>>> is not a valid Discover credit card number.',  # noqa: E501
    ):
        DiscoverCreditCardValueObject(value='6011111111111118')


@mark.unit_testing
def test_discover_credit_card_value_object_invalid_processed_value() -> None:
    """
    Test DiscoverCreditCardValueObject defensive validation branch for invalid processed values.
    """
    card: Any = DiscoverCreditCardValueObject(value='6011-1111-1111-1117')

    with assert_raises(
        expected_exception=ValueError,
        match=r'DiscoverCreditCardValueObject value <<<6011111111111117>>> is not a valid Discover credit card number.',  # noqa: E501
    ):
        card._ensure_value_follows_validation_regex(value='6011111111111117', processed_value='INVALID')
