# Reusable Value Object Catalog

Use this file to select built-in validators before writing custom classes. Verify the installed package version when
working in a consuming project.

## Root Public API

```python
from value_object_pattern import (
    BaseModel,
    EnumerationValueObject,
    SecretValueObject,
    UnionValueObject,
    ValueObject,
    process,
    validation,
)
```

Compose non-generic `SecretValueObject` with any typed value-object base that requires display redaction. It works in either inheritance order while the other base retains typing, validation, processing, and raw primitive conversion.

```python
from value_object_pattern import SecretValueObject
from value_object_pattern.usables import BooleanValueObject, StringValueObject


class SecretString(SecretValueObject, StringValueObject):
    pass


class SecretBoolean(BooleanValueObject, SecretValueObject):
    pass
```

## Primitive Imports

Most primitive value objects are re-exported from `value_object_pattern.usables`.

```python
from value_object_pattern.usables import (
    Base16StringValueObject,
    Base32StringValueObject,
    Base36StringValueObject,
    Base56StringValueObject,
    Base58StringValueObject,
    Base64StringValueObject,
    HexadecimalStringValueObject,
)
```

Category-specific imports are also available:

```python
from value_object_pattern.usables.primitives.string import SnakeCaseStringValueObject
from value_object_pattern.usables.primitives.integer import EvenIntegerValueObject
```

## Primitive Value Objects

Strings:

| Value Object | Rule |
| --- | --- |
| `StringValueObject` | Exact `str` values. |
| `NotEmptyStringValueObject` | Rejects empty strings. |
| `TrimmedStringValueObject` | Rejects leading/trailing whitespace. |
| `HexadecimalStringValueObject` / `Base16StringValueObject` | Valid Base16 strings in either letter case. |
| `Base32StringValueObject` | Canonical padded Base32 strings in either letter case. |
| `Base36StringValueObject` | Uppercase Base36 alphabet strings. |
| `Base56StringValueObject` | Ambiguity-free Base56 alphabet strings. |
| `Base58StringValueObject` | Bitcoin Base58 alphabet strings. |
| `Base64StringValueObject` | Canonical standard Base64 strings, including the empty encoding. |
| `AlphaStringValueObject` | Alphabetic strings. |
| `AlphanumericStringValueObject` | Alphabetic and numeric characters. |
| `DigitStringValueObject` | Digit-only strings. |
| `PrintableStringValueObject` | Printable strings. |
| `LowercaseStringValueObject` | Lowercase strings. |
| `UppercaseStringValueObject` | Uppercase strings. |
| `SnakeCaseStringValueObject` | `snake_case` strings. |
| `ScreamingSnakeCaseStringValueObject` | `SCREAMING_SNAKE_CASE` strings. |
| `KebabCaseStringValueObject` | `kebab-case` strings. |
| `CamelCaseStringValueObject` | `camelCase` strings. |
| `PascalCaseStringValueObject` | `PascalCase` strings. |

Numbers, booleans, bytes, and none:

| Value Object | Rule |
| --- | --- |
| `IntegerValueObject` | Exact `int` values. |
| `PositiveIntegerValueObject` | Integers greater than zero. |
| `PositiveOrZeroIntegerValueObject` | Integers greater than or equal to zero. |
| `NegativeIntegerValueObject` | Integers lower than zero. |
| `NegativeOrZeroIntegerValueObject` | Integers lower than or equal to zero. |
| `EvenIntegerValueObject` | Even integers. |
| `OddIntegerValueObject` | Odd integers. |
| `FloatValueObject` | Exact `float` values. |
| `PositiveFloatValueObject` | Floats greater than zero. |
| `PositiveOrZeroFloatValueObject` | Floats greater than or equal to zero. |
| `NegativeFloatValueObject` | Floats lower than zero. |
| `NegativeOrZeroFloatValueObject` | Floats lower than or equal to zero. |
| `BooleanValueObject` | Exact `bool` values. |
| `TrueValueObject` | Only `True`. |
| `FalseValueObject` | Only `False`. |
| `BytesValueObject` | Exact `bytes` values. |
| `NoneValueObject` | Only `None`. |
| `NotNoneValueObject` | Rejects `None`. |

## Date And Time

```python
from value_object_pattern.usables.dates import (
    DateValueObject,
    DatetimeValueObject,
    StringDateValueObject,
    StringDatetimeValueObject,
    StringTimezoneValueObject,
    TimezoneValueObject,
)
```

| Value Object | Rule / Helpers |
| --- | --- |
| `DateValueObject` | Exact `datetime.date`; helpers: `is_today`, `is_later_than`, `is_in_range`, `calculate_age`. |
| `DatetimeValueObject` | Exact `datetime.datetime`; helpers: `is_now`, `is_today`, `is_later_than`, `is_in_range`, `calculate_age`. |
| `StringDateValueObject` | String dates in the configured package format; same date helpers. |
| `StringDatetimeValueObject` | String datetimes in the configured package format; same datetime helpers. |
| `TimezoneValueObject` | `tzinfo` objects. |
| `StringTimezoneValueObject` | Timezone names as strings. |

Pass explicit `reference_date` or `reference_datetime` in tests.

## UUID Identifiers

```python
from value_object_pattern.usables.identifiers.uuid import StringUuidV4ValueObject, UuidV4ValueObject
```

| Family | Value Objects |
| --- | --- |
| Any supported UUID | `UuidValueObject`, `StringUuidValueObject` |
| UUID objects | `UuidV1ValueObject`, `UuidV3ValueObject`, `UuidV4ValueObject`, `UuidV5ValueObject`, `UuidV6ValueObject`, `UuidV7ValueObject`, `UuidV8ValueObject` |
| UUID strings | `StringUuidV1ValueObject`, `StringUuidV3ValueObject`, `StringUuidV4ValueObject`, `StringUuidV5ValueObject`, `StringUuidV6ValueObject`, `StringUuidV7ValueObject`, `StringUuidV8ValueObject` |

Use exact versioned classes when UUID version matters.

## World Identifiers

```python
from value_object_pattern.usables.identifiers.world import Iso3166Alpha2CodeValueObject, VinValueObject
```

| Value Object | Rule / Helpers |
| --- | --- |
| `CountryTldValueObject` | Country top-level domains; conversion helpers to ISO and phone-code values. |
| `Iso3166Alpha2CodeValueObject` | ISO 3166 alpha-2; conversion helpers to alpha-3, numeric, phone code, and TLD. |
| `Iso3166Alpha3CodeValueObject` | ISO 3166 alpha-3; conversion helpers to alpha-2, numeric, phone code, and TLD. |
| `Iso3166NumericCodeValueObject` | ISO 3166 numeric code; conversion helpers to alpha-2, alpha-3, phone code, and TLD. |
| `PhoneCodeValueObject` | International phone calling code; conversion helpers to ISO and TLD values. |
| `VinValueObject` | Vehicle identification numbers; stores uppercase. |

These validators check syntax/catalog/checksum-style rules. They do not prove legal status or ownership.

## Spanish Identifiers

```python
from value_object_pattern.usables.identifiers.world.europe.spain import DniValueObject, NifValueObject
```

| Value Object | Rule |
| --- | --- |
| `DniValueObject` | Spanish DNI identifiers. |
| `NieValueObject` | Spanish NIE identifiers. |
| `NifValueObject` | Spanish NIF identifiers. |
| `NussValueObject` | Spanish social security identifiers. |
| `PassportValueObject` | Spanish passport-like values. |
| `PhoneNumberValueObject` | Spanish phone number values. |
| `VehiclePlateValueObject` | Any supported Spanish vehicle plate format. |

Specific Spanish vehicle plate validators are available from
`value_object_pattern.usables.identifiers.world.europe.spain.plates`, including ordinary, temporary, official, service,
diplomatic, international, historical, provincial, and ministry formats. Use `VehiclePlateValueObject` when any
supported format is acceptable.

## Internet

```python
from value_object_pattern.usables.internet import (
    DomainOrLocalhostValueObject,
    DomainValueObject,
    EmailAddressValueObject,
    PortValueObject,
)
from value_object_pattern.usables.internet.uri import HttpsUrlValueObject, UrlValueObject
```

URLs, hosts, and domains:

| Value Object | Rule |
| --- | --- |
| `UrlValueObject` | Validates URL syntax and stores normalized URL form. |
| `HttpUrlValueObject` | HTTP URLs only. |
| `HttpsUrlValueObject` | HTTPS URLs only. |
| `HttpHttpsUrlValueObject` | HTTP or HTTPS URLs. |
| `HostValueObject` | Host values; helpers: `is_domain`, `is_ipv4_address`, `is_ipv6_address`. |
| `DomainOrLocalhostValueObject` | Domain values or `localhost`. |
| `DomainValueObject` | Domain labels and top-level domains. |

Addresses, networks, and ports:

| Value Object | Rule / Helpers |
| --- | --- |
| `IpAddressValueObject` | IPv4 or IPv6 address values; helpers: `is_ipv4_address`, `is_ipv6_address`. |
| `Ipv4AddressValueObject` | IPv4 address values; helpers for reserved, private, global, multicast, unspecified, loopback, link-local, plus `UNSPECIFIED` and `LOOPBACK`. |
| `Ipv6AddressValueObject` | IPv6 address values; same address-category helpers and constants. |
| `Ipv4NetworkValueObject` | IPv4 network values; helpers: `hosts`, `all_addresses`, `get_network`, `get_broadcast`, `get_mask`, `get_number_addresses`. |
| `Ipv6NetworkValueObject` | IPv6 network values; helpers: `hosts`, `all_addresses`, `get_network`, `get_mask`, `get_number_addresses`. |
| `MacAddressValueObject` | Supported MAC address formats; conversion helpers to raw, universal, Windows, Cisco, and space-separated formats. |
| `PortValueObject` | Valid TCP/UDP port numbers. |

Keys, slugs, and metadata:

| Value Object | Rule |
| --- | --- |
| `SnakeCaseKeyValueObject` | Snake-case key strings. |
| `KebabCaseKeyValueObject` | Kebab-case key strings. |
| `SlugValueObject` | Slug strings. |
| `EmailAddressValueObject` | Email address strings; stores lowercase. |
| `AwsCloudRegionValueObject` | AWS cloud region identifiers from the package catalog. |
| `UserAgentValueObject` | User-agent strings. |
| `ImeiValueObject` | IMEI values under `value_object_pattern.usables.internet.mobile`. |

MAC format-specific classes live under `value_object_pattern.usables.internet.mac_addresses`.

## Money

```python
from value_object_pattern.usables.money import CreditCardValueObject, IbanValueObject
from value_object_pattern.usables.money.credit_cards import VisaCreditCardValueObject
```

| Value Object | Rule |
| --- | --- |
| `IbanValueObject` | IBAN format and checksum. |
| `CreditCardValueObject` | Any supported credit-card brand format. |
| `VisaCreditCardValueObject` | Visa shape and Luhn checksum. |
| `MastercardCreditCardValueObject` | Mastercard shape and Luhn checksum. |
| `AmexCreditCardValueObject` | American Express shape and Luhn checksum. |
| `DiscoverCreditCardValueObject` | Discover shape and Luhn checksum. |

Never treat payment-shaped validation as authorization, ownership proof, or permission to store sensitive payment data.
