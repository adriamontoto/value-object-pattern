# Money Value Objects

Money value objects validate currency codes and payment-shaped identifiers such as IBANs and credit-card numbers.

## Imports

```python
from value_object_pattern.usables.money import CreditCardValueObject, CurrencyCodeValueObject, IbanValueObject
from value_object_pattern.usables.money.credit_cards import VisaCreditCardValueObject
```

## Catalog

| Value Object                      | Rule                                                                    |
| --------------------------------- | ----------------------------------------------------------------------- |
| `CurrencyCodeValueObject`         | Validates codes in the packaged ISO 4217 List One catalog and stores uppercase. |
| `IbanValueObject`                 | Validates IBAN format, MOD-97 checksum, and Spanish CCC control digits. |
| `CreditCardValueObject`           | Accepts any supported credit-card brand format.                         |
| `VisaCreditCardValueObject`       | Validates Visa card number shape and Luhn checksum.                     |
| `MastercardCreditCardValueObject` | Validates Mastercard number shape and Luhn checksum.                    |
| `AmexCreditCardValueObject`       | Validates American Express number shape and Luhn checksum.              |
| `DiscoverCreditCardValueObject`   | Validates Discover number shape and Luhn checksum.                      |

## Example

```python
from value_object_pattern.usables.money import CreditCardValueObject, CurrencyCodeValueObject

card = CreditCardValueObject(value="4545537331205356")
currency = CurrencyCodeValueObject(value="eur")

assert card.value == "4545537331205356"
assert currency.value == "EUR"
```

The packaged currency catalog contains current List One currency and fund codes; historical codes are rejected. These
validators do not prove account/card ownership or authorize payment, and display validation does not make payment data
safe to store.
