# Identifier Value Objects

Identifier value objects validate stable external identifiers such as UUIDs, country codes, phone codes, vehicle
identifiers, and country-specific document numbers.

## UUIDs

UUID validators are available for object and string forms:

```python
from value_object_pattern.usables.identifiers.uuid import StringUuidV4ValueObject, UuidV4ValueObject
```

| Family | Value Objects |
| --- | --- |
| Any supported UUID | `UuidValueObject`, `StringUuidValueObject` |
| Versioned UUID objects | `UuidV1ValueObject`, `UuidV3ValueObject`, `UuidV4ValueObject`, `UuidV5ValueObject`, `UuidV6ValueObject`, `UuidV7ValueObject`, `UuidV8ValueObject` |
| Versioned UUID strings | `StringUuidV1ValueObject`, `StringUuidV3ValueObject`, `StringUuidV4ValueObject`, `StringUuidV5ValueObject`, `StringUuidV6ValueObject`, `StringUuidV7ValueObject`, `StringUuidV8ValueObject` |

## World Identifiers

```python
from value_object_pattern.usables.identifiers.world import Iso3166Alpha2CodeValueObject, VinValueObject
```

| Value Object | Rule |
| --- | --- |
| `CountryTldValueObject` | Validates country top-level domains. |
| `Iso3166Alpha2CodeValueObject` | Validates ISO 3166 alpha-2 country codes. |
| `Iso3166Alpha3CodeValueObject` | Validates ISO 3166 alpha-3 country codes. |
| `Iso3166NumericCodeValueObject` | Validates ISO 3166 numeric country codes. |
| `PhoneCodeValueObject` | Validates international phone calling codes. |
| `VinValueObject` | Validates vehicle identification numbers and stores them uppercase. |

## Spanish Identifiers

```python
from value_object_pattern.usables.identifiers.world.europe.spain import DniValueObject, NifValueObject
```

| Value Object | Rule |
| --- | --- |
| `DniValueObject` | Validates Spanish DNI identifiers. |
| `NieValueObject` | Validates Spanish NIE identifiers. |
| `NifValueObject` | Validates Spanish NIF identifiers. |
| `NussValueObject` | Validates Spanish social security identifiers. |
| `PassportValueObject` | Validates Spanish passport-like values. |
| `PhoneNumberValueObject` | Validates Spanish phone number values. |
| `VehiclePlateValueObject` | Accepts any supported Spanish vehicle plate format. |

## Spanish Vehicle Plates

Specific vehicle plate validators are available from
`value_object_pattern.usables.identifiers.world.europe.spain.plates`.

| Family | Examples |
| --- | --- |
| Ordinary plates | `OrdinaryVehiclePlateValueObject`, `OrdinaryTruckVehiclePlateValueObject`, `TwoWheelsVehiclePlateValueObject` |
| Temporary plates | `TemporalCompanyNotRegisteredVehiclePlateValueObject`, `TemporalCompanyRegisteredVehiclePlateValueObject`, `TemporalPrivateIndividualVehiclePlateValueObject` |
| Official and service plates | `CivilGuardVehiclePlateValueObject`, `NationalPoliceVehiclePlateValueObject`, `StateMotorPoolVehiclePlateValueObject`, `NavyVehiclePlateValueObject`, `ArmyVehiclePlateValueObject`, `AirForceVehiclePlateValueObject` |
| Diplomatic and international plates | `DiplomaticCorpsVehiclePlateValueObject`, `ConsularCorpsVehiclePlateValueObject`, `InternationalOrganizationVehiclePlateValueObject` |
| Other supported formats | `AdministrativeTechnicianVehiclePlateValueObject`, `CanariasPoliceVehiclePlateValueObject`, `CatalanPoliceVehiclePlateValueObject`, `EspecialVehiclePlateValueObject`, `HistoricalVehiclePlateValueObject`, `MinistryDevelopmentVehiclePlateValueObject`, `MinistryEnvironmentVehiclePlateValueObject`, `ProvincialSystemVehiclePlateValueObject` |

## Guidance

- Use exact versioned UUID value objects when the UUID version matters.
- Use aggregate validators such as `VehiclePlateValueObject` when any supported format is acceptable.
- Treat these validators as syntactic and checksum validation helpers; they do not prove ownership, identity, or legal
  status.
