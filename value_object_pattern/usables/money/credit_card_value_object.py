"""
CreditCardValueObject value object.
"""

from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.models.value_object import ValueObject
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .credit_cards import (
    AmexCreditCardValueObject,
    DiscoverCreditCardValueObject,
    MastercardCreditCardValueObject,
    VisaCreditCardValueObject,
)


class CreditCardValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    CreditCardValueObject value object ensures the provided value is a valid credit card number.

    Example:
    ```python
    from value_object_pattern.usables.money import CreditCardValueObject

    card = CreditCardValueObject(value='4545537331205356')

    print(repr(card))
    # >>> CreditCardValueObject(value=4545537331205356)
    ```
    """

    _CREDIT_CARD_VARIATIONS: tuple[type[ValueObject[str]], ...] = (
        AmexCreditCardValueObject,
        DiscoverCreditCardValueObject,
        MastercardCreditCardValueObject,
        VisaCreditCardValueObject,
    )

    @process(order=0)
    def _ensure_value_is_formatted(self, value: str) -> str:  # type: ignore[return]
        """
        Ensures the value object `value` is stored formatted.

        Args:
            value (str): The provided value.

        Returns:
            str: Formatted `value`.
        """
        for variation in self._CREDIT_CARD_VARIATIONS:
            try:
                return variation(value=value).value

            except Exception:  # noqa: S112
                continue

    @validation(order=0)
    def _ensure_value_is_credit_card(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid credit card number.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid credit card number.
        """
        for variation in self._CREDIT_CARD_VARIATIONS:
            try:
                variation(value=value)
                return

            except Exception:  # noqa: S112
                continue

        self._raise_value_is_not_credit_card(value=value)

    def _raise_value_is_not_credit_card(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid credit card number.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid credit card number.
        """
        raise ValueError(f'CreditCardValueObject value <<<{value}>>> is not a valid credit card number.')
