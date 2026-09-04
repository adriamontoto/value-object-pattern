# Identifier Value Objects

Identifier value objects validate stable external identifiers such as UUIDs, ULIDs, language tags, country codes,
phone codes, vehicle identifiers, and country-specific document numbers.

## ULIDs

```python
from value_object_pattern.usables.identifiers import UlidValueObject


identifier = UlidValueObject(value="01arz3ndektsv4rrffq69g5fav")

assert identifier.value == "01ARZ3NDEKTSV4RRFFQ69G5FAV"
```

`UlidValueObject` accepts the canonical 26-character Crockford Base32 representation, rejects encodings above the
128-bit ULID maximum, and stores valid input in uppercase. It validates existing identifiers; it does not generate
them.

## UUIDs

UUID validators are available for object and string forms:

```python
from value_object_pattern.usables.identifiers.uuid import StringUuidV4ValueObject, UuidV4ValueObject
```

| Family                 | Value Objects                                                                                                                                                                               |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Any supported UUID     | `UuidValueObject`, `StringUuidValueObject`                                                                                                                                                  |
| Versioned UUID objects | `UuidV1ValueObject`, `UuidV3ValueObject`, `UuidV4ValueObject`, `UuidV5ValueObject`, `UuidV6ValueObject`, `UuidV7ValueObject`, `UuidV8ValueObject`                                           |
| Versioned UUID strings | `StringUuidV1ValueObject`, `StringUuidV3ValueObject`, `StringUuidV4ValueObject`, `StringUuidV5ValueObject`, `StringUuidV6ValueObject`, `StringUuidV7ValueObject`, `StringUuidV8ValueObject` |

## World Identifiers

```python
from value_object_pattern.usables.identifiers.world import (
    Bcp47LanguageTagValueObject,
    Iso3166Alpha2CodeValueObject,
    VinValueObject,
)
```

| Value Object                       | Rule                                                                                                               |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `Bcp47LanguageTagValueObject`      | Validates BCP 47 language tags and normalizes language, script, region, extension, and private-use casing.         |
| `CountryTldValueObject`            | Validates country top-level domains.                                                                               |
| `Iso3166Alpha2CodeValueObject`     | Validates ISO 3166 alpha-2 country codes.                                                                          |
| `Iso3166Alpha3CodeValueObject`     | Validates ISO 3166 alpha-3 country codes.                                                                          |
| `Iso3166NumericCodeValueObject`    | Validates ISO 3166 numeric country codes.                                                                          |
| `PhoneCodeValueObject`             | Validates international phone calling codes.                                                                       |
| `VinValueObject`                   | Validates vehicle identification numbers and stores them uppercase.                                                |

```python
language = Bcp47LanguageTagValueObject(value="ZH-hant-tw")

assert language.value == "zh-Hant-TW"
```

BCP 47 uses hyphens; locale spellings such as `en_US` are rejected. Core subtags are checked against the packaged IANA
registry data, while extension and private-use sequences are syntax-checked.

## Spanish Identifiers

```python
from value_object_pattern.usables.identifiers.world.europe.spain import DniValueObject, NifValueObject
```

| Value Object              | Rule                                                |
| ------------------------- | --------------------------------------------------- |
| `DniValueObject`          | Validates Spanish DNI identifiers.                  |
| `NieValueObject`          | Validates Spanish NIE identifiers.                  |
| `NifValueObject`          | Validates Spanish NIF identifiers.                  |
| `NussValueObject`         | Validates Spanish social security identifiers.      |
| `PassportValueObject`     | Validates Spanish passport-like values.             |
| `PhoneNumberValueObject`  | Validates Spanish phone number values.              |
| `VehiclePlateValueObject` | Accepts any supported Spanish vehicle plate format. |

## Spanish Vehicle Plates

Specific vehicle plate validators are available from
`value_object_pattern.usables.identifiers.world.europe.spain.plates`.

| Family                              | Examples                                                                                                                                                                                                                                                                                                                                          |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Ordinary plates                     | `OrdinaryVehiclePlateValueObject`, `OrdinaryTruckVehiclePlateValueObject`, `TwoWheelsVehiclePlateValueObject`                                                                                                                                                                                                                                     |
| Temporary plates                    | `TemporalCompanyNotRegisteredVehiclePlateValueObject`, `TemporalCompanyRegisteredVehiclePlateValueObject`, `TemporalPrivateIndividualVehiclePlateValueObject`                                                                                                                                                                                     |
| Official and service plates         | `CivilGuardVehiclePlateValueObject`, `NationalPoliceVehiclePlateValueObject`, `StateMotorPoolVehiclePlateValueObject`, `NavyVehiclePlateValueObject`, `ArmyVehiclePlateValueObject`, `AirForceVehiclePlateValueObject`                                                                                                                            |
| Diplomatic and international plates | `DiplomaticCorpsVehiclePlateValueObject`, `ConsularCorpsVehiclePlateValueObject`, `InternationalOrganizationVehiclePlateValueObject`                                                                                                                                                                                                              |
| Other supported formats             | `AdministrativeTechnicianVehiclePlateValueObject`, `CanariasPoliceVehiclePlateValueObject`, `CatalanPoliceVehiclePlateValueObject`, `EspecialVehiclePlateValueObject`, `HistoricalVehiclePlateValueObject`, `MinistryDevelopmentVehiclePlateValueObject`, `MinistryEnvironmentVehiclePlateValueObject`, `ProvincialSystemVehiclePlateValueObject` |

## Guidance

- Use exact versioned UUID value objects when the UUID version matters.
- Use `UlidValueObject` to validate a supplied ULID, not to generate one.
- Use aggregate validators such as `VehiclePlateValueObject` when any supported format is acceptable.
- Treat these validators as syntactic and checksum validation helpers; they do not prove ownership, identity, or legal
  status.
