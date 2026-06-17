# Examples And Testing Reference

Use this file when writing code examples, tests, or reviews for projects using `value-object-pattern`.

## Custom Value Object Example

```python
from value_object_pattern import validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class ProductSku(NotEmptyStringValueObject, TrimmedStringValueObject):
    @validation(order=0)
    def _ensure_value_has_sku_prefix(self, value: str) -> None:
        if not value.startswith('sku-'):
            raise ValueError('ProductSku value must start with "sku-".')
```

Use multiple inheritance with reusable bases when each base contributes a reusable validation rule. Add a custom
validator only for the domain-specific rule.

## Normalization Example

```python
from value_object_pattern import process
from value_object_pattern.usables import StringValueObject


class NormalizedEmail(StringValueObject):
    @process(order=0)
    def _strip(self, value: str) -> str:
        return value.strip()

    @process(order=1)
    def _lower(self, value: str) -> str:
        return value.lower()
```

Use `@process` only for deterministic transformations. Do not use it for remote lookups, random values, current time, or
stateful operations.

## Aggregate Example

```python
from value_object_pattern import BaseModel
from value_object_pattern.usables import NotEmptyStringValueObject, PositiveIntegerValueObject
from value_object_pattern.usables.internet import EmailAddressValueObject


class UserRegistration(BaseModel):
    def __init__(
        self,
        name: NotEmptyStringValueObject,
        email: EmailAddressValueObject,
        age: PositiveIntegerValueObject,
    ) -> None:
        self.name = name
        self.email = email
        self.age = age
```

Inbound boundary:

```python
registration = UserRegistration.from_primitives(
    primitives={
        'name': 'Ada',
        'email': 'ADA@example.com',
        'age': 42,
    },
)
```

Outbound boundary:

```python
payload = registration.to_primitives()
```

## Pytest Patterns

```python
import pytest


def test_product_sku_accepts_prefixed_value() -> None:
    sku = ProductSku(value='sku-123')

    assert sku.value == 'sku-123'


def test_product_sku_rejects_missing_prefix() -> None:
    with pytest.raises(ValueError, match='ProductSku value must start with "sku-"'):
        ProductSku(value='123')
```

For normalization:

```python
def test_normalized_email_strips_and_lowers_value() -> None:
    email = NormalizedEmail(value='  ADA@example.COM  ')

    assert email.value == 'ada@example.com'
```

For conversion:

```python
def test_user_registration_from_primitives_builds_value_objects() -> None:
    registration = UserRegistration.from_primitives(
        primitives={
            'name': 'Ada',
            'email': 'ada@example.com',
            'age': 42,
        },
    )

    assert isinstance(registration.name, NotEmptyStringValueObject)
    assert isinstance(registration.email, EmailAddressValueObject)
    assert isinstance(registration.age, PositiveIntegerValueObject)
    assert registration.to_primitives() == {'age': 42, 'email': 'ada@example.com', 'name': 'Ada'}
```

## Test Checklist

- Valid construction stores the expected `.value`.
- Invalid primitive type is rejected when the base class is type-specific.
- Invalid domain value is rejected with a clear exception type and message.
- Normalization output is asserted when `@process` is used.
- Equality is tested with same concrete class and different concrete classes when behavior matters.
- Immutability is tested only if the consuming project relies on that guarantee directly.
- `BaseModel.from_primitives()` and `to_primitives()` are tested at API/persistence boundaries.
- Collections are tested for helper return values and non-mutation of the original instance.
- Date/datetime helpers receive explicit reference values.
- `SecretStringValueObject` display redaction is tested separately from stored `.value`.

## Review Prompts For Agents

When reviewing code that uses this package, check:

- Could an existing reusable value object replace custom validation?
- Is a custom value object named after the domain concept?
- Are primitive values unpacked too early with `.value`?
- Are constructor annotations precise enough for `BaseModel.from_primitives()`?
- Are invalid examples deterministic and representative?
- Are secret-like values accidentally exposed through `repr`, `str`, logs, or primitive conversion?
- Are validators free of side effects?
- Are processors deterministic and ordered?
