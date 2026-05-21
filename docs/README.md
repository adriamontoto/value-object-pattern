# Value Object Pattern Documentation

Value Object Pattern provides typed building blocks for immutable value objects, reusable validators, primitive
conversion, and small domain models.

Use this page as the documentation hub:

| Guide | Purpose |
| --- | --- |
| [Usage Guide](usage/README.md) | Define custom value objects, validators, processors, and model composition. |
| [Catalog](catalog/README.md) | Feature map by reusable value-object category. |
| [Primitive Catalog](catalog/primitives/README.md) | Strings, numbers, booleans, bytes, and none value objects. |
| [Date Catalog](catalog/dates/README.md) | Date, datetime, and timezone value objects. |
| [Identifier Catalog](catalog/identifiers/README.md) | UUID, world, Spanish, and vehicle-plate value objects. |
| [Internet Catalog](catalog/internet/README.md) | URL, host, address, key, and metadata value objects. |
| [Money Catalog](catalog/money/README.md) | IBAN and credit-card value objects. |
| [Conversion Guide](conversion/README.md) | Convert value objects, models, enums, collections, and unions to/from primitives. |
| [Data Safety](data-safety/README.md) | Security and correctness boundaries for validation and redacted display values. |

## Public Import Shapes

Core imports:

```python
from value_object_pattern import BaseModel, EnumerationValueObject, UnionValueObject, ValueObject, process, validation
```

Reusable value-object imports:

```python
from value_object_pattern.usables import NotEmptyStringValueObject, PositiveIntegerValueObject
```

Collection value-object imports:

```python
from value_object_pattern.models.collections import DictValueObject, ListValueObject
```

## Recommended Flow

1. Use reusable value objects when an existing validator matches the domain rule.
2. Create a custom `ValueObject[T]` when the rule is domain-specific.
3. Add `@validation` hooks for rejection rules.
4. Add `@process` hooks for deterministic normalization.
5. Use `BaseModel.from_primitives()` and `to_primitives()` at API, storage, or messaging boundaries.
6. Keep secret handling explicit; display redaction is not encryption.
