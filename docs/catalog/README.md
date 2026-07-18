# Value Object Catalog

This catalog summarizes the reusable value-object surface by category. Common primitive validators are exported from
`value_object_pattern.usables`; specialized validators live under their domain packages.

For deeper category references, use:

- [Primitive Value Objects](primitives/README.md)
- [Date And Time Value Objects](dates/README.md)
- [Identifier Value Objects](identifiers/README.md)
- [Internet Value Objects](internet/README.md)
- [Money Value Objects](money/README.md)

## Core Models

| Model | Purpose |
| --- | --- |
| `ValueObject[T]` | Immutable validated wrapper for one value. |
| `EnumerationValueObject[E]` | Enum-backed value object accepting enum members or raw enum values. |
| `UnionValueObject[T]` | Value object constrained by a union annotation; supports named subclasses and inline construction. |
| `BaseModel` | Aggregate-like model with primitive conversion and public-state representation. |
| `ListValueObject[T]` | Typed immutable list wrapper; supports named subclasses and inline construction. |
| `DictValueObject[K, V]` | Typed immutable dictionary wrapper; supports named subclasses and inline construction. |

## Primitive Value Objects

| Area | Examples |
| --- | --- |
| Strings | `StringValueObject`, `NotEmptyStringValueObject`, `TrimmedStringValueObject`, `SecretStringValueObject` |
| String formats | lower/upper case, snake case, kebab case, camel case, pascal case, alpha, alphanumeric, digit |
| Integers | integer, positive, positive-or-zero, negative, negative-or-zero, even, odd |
| Floats | float, positive, positive-or-zero, negative, negative-or-zero |
| Booleans | boolean, true, false |
| Bytes and none | bytes, none, not-none |

Import examples:

```python
from value_object_pattern.usables import NotEmptyStringValueObject, PositiveIntegerValueObject
```

See [Primitive Value Objects](primitives/README.md) for the complete primitive family.

## Dates And Time

Reusable date/time validators include:

- `DateValueObject`
- `DatetimeValueObject`
- `StringDateValueObject`
- `StringDatetimeValueObject`
- `TimezoneValueObject`
- `StringTimezoneValueObject`

Import examples:

```python
from value_object_pattern.usables.dates import DateValueObject, StringTimezoneValueObject
```

See [Date And Time Value Objects](dates/README.md) for conversion and comparison notes.

## Identifiers

Identifier validators cover:

- UUID objects and UUID strings for supported UUID versions.
- World identifiers such as ISO 3166 alpha-2, alpha-3, numeric codes, phone codes, country TLDs, and VIN values.
- Spanish identifiers such as DNI, NIE, NIF, NUSS, passport, phone numbers, and vehicle plates.

Import examples:

```python
from value_object_pattern.usables.identifiers.uuid import StringUuidV4ValueObject, UuidV4ValueObject
from value_object_pattern.usables.identifiers.world import Iso3166Alpha2CodeValueObject
```

See [Identifier Value Objects](identifiers/README.md) for UUID, world, Spanish, and vehicle-plate validators.

## Internet

Internet validators cover:

| Area | Examples |
| --- | --- |
| URLs and hosts | `UrlValueObject`, `HttpUrlValueObject`, `HttpsUrlValueObject`, `HostValueObject`, `DomainOrLocalhostValueObject`, `DomainValueObject` |
| Addresses and networks | IPv4, IPv6, IP address, IPv4 network, IPv6 network |
| Network metadata | MAC address formats, ports, AWS cloud regions, user agents |
| Keys and slugs | snake-case keys, kebab-case keys, slugs |
| Contact-like values | email addresses, IMEI values |

Import examples:

```python
from value_object_pattern.usables.internet import DomainOrLocalhostValueObject, DomainValueObject, EmailAddressValueObject
from value_object_pattern.usables.internet.uri import UrlValueObject
```

See [Internet Value Objects](internet/README.md) for URL, host, address, key, and network boundaries.

## Money

Money validators include:

- `IbanValueObject`
- `CreditCardValueObject`
- Brand-specific credit card value objects for supported brands.

Import examples:

```python
from value_object_pattern.usables.money import CreditCardValueObject, IbanValueObject
```

See [Money Value Objects](money/README.md) for IBAN and credit-card validation notes.

## Catalog Checklist

- Use reusable validators for common primitive and format rules.
- Use domain packages for specialized identifiers, internet, and money validators.
- Use `SecretStringValueObject` only for display redaction, not secret storage.
- Create custom value objects for domain-specific rules that are not generic reusable validators.
