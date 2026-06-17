"""
Test CreditCardValueObject value object.
"""

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.money import CreditCardValueObject


@mark.unit_testing
def test_credit_card_value_object_accepts_visa_card() -> None:
    """
    Test CreditCardValueObject value object accepts Visa cards.
    """
    card = CreditCardValueObject(value='4111-1111-1111-1111')

    assert type(card.value) is str
    assert card.value == '4111111111111111'


@mark.unit_testing
def test_credit_card_value_object_accepts_mastercard_card() -> None:
    """
    Test CreditCardValueObject value object accepts Mastercard cards.
    """
    assert CreditCardValueObject(value='5555-5555-5555-4444').value == '5555555555554444'


@mark.unit_testing
def test_credit_card_value_object_accepts_amex_card() -> None:
    """
    Test CreditCardValueObject value object accepts Amex cards.
    """
    assert CreditCardValueObject(value='3714-496353-98431').value == '371449635398431'


@mark.unit_testing
def test_credit_card_value_object_accepts_discover_card() -> None:
    """
    Test CreditCardValueObject value object accepts Discover cards.
    """
    assert CreditCardValueObject(value='6011-1111-1111-1117').value == '6011111111111117'


@mark.unit_testing
def test_credit_card_value_object_invalid_value() -> None:
    """
    Test CreditCardValueObject value object raises ValueError when value is not a supported credit card.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'CreditCardValueObject value <<<0000-0000-0000-0000>>> is not a valid credit card number.',
    ):
        CreditCardValueObject(value='0000-0000-0000-0000')


@mark.unit_testing
def test_credit_card_value_object_formatting_returns_none_for_unknown_card() -> None:
    """
    Test CreditCardValueObject defensive formatting branch for unknown card variations.
    """
    card = CreditCardValueObject(value='4111-1111-1111-1111')

    assert card._ensure_value_is_formatted(value='0000-0000-0000-0000') is None
