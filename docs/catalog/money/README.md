# Money Value Objects

Money value objects validate payment-shaped identifiers such as IBANs and credit-card numbers.

## Imports

```python
from value_object_pattern.usables.money import CreditCardValueObject, IbanValueObject
from value_object_pattern.usables.money.credit_cards import VisaCreditCardValueObject
```

## Catalog

| Value Object | Rule |
| --- | --- |
| `IbanValueObject` | Validates IBAN format and checksum. |
| `CreditCardValueObject` | Accepts any supported credit-card brand format. |
| `VisaCreditCardValueObject` | Validates Visa card number shape and Luhn checksum. |
| `MastercardCreditCardValueObject` | Validates Mastercard number shape and Luhn checksum. |
| `AmexCreditCardValueObject` | Validates American Express number shape and Luhn checksum. |
| `DiscoverCreditCardValueObject` | Validates Discover number shape and Luhn checksum. |

## Example

```python
from value_object_pattern.usables.money import CreditCardValueObject

card = CreditCardValueObject(value='4545537331205356')

assert card.value == '4545537331205356'
```