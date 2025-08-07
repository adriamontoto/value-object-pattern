"""
CreditCardValueObject value object.
"""

from re import Pattern
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.models.value_object import ValueObject
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .credit_cards import AmexValueObject, DiscoverValueObject, MasterCardValueObject, VisaValueObject


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

    __CREDIT_CARD_VALUE_OBJECT_VARIATIONS: tuple[type[ValueObject[str]], ...] = (
        AmexValueObject,
        DiscoverValueObject,
        MasterCardValueObject,
        VisaValueObject,
    )

    @process(order=0)
    def _ensure_value_is_stored_formatted(self, value: str) -> str:  # type: ignore[return]
        """
        Ensures the value object `value` is stored formatted.

        Args:
            value (str): The provided value.

        Returns:
            str: Formatted `value`.
        """
        for variation in self.__CREDIT_CARD_VALUE_OBJECT_VARIATIONS:
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
        for variation in self.__CREDIT_CARD_VALUE_OBJECT_VARIATIONS:
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

    @classmethod
    def regexs(cls) -> list[Pattern[str]]:
        """
        Returns a list of regex patterns used for validation.

        Returns:
            list[Pattern[str]]: List of regex patterns.
        """
        return [variation.regexs() for variation in cls.__CREDIT_CARD_VALUE_OBJECT_VARIATIONS]  # type: ignore[attr-defined]
