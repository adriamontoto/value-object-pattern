# Core API Reference

Use this file when creating or reviewing custom value objects.

## Imports

```python
from value_object_pattern import BaseModel, EnumerationValueObject, UnionValueObject, ValueObject, process, validation
from value_object_pattern.models.collections import DictValueObject, ListValueObject
```

## ValueObject

`ValueObject[T]` is the base immutable wrapper for exactly one value.

Observed behavior in `value_object_pattern` 1.31.0:

- Construct with keyword arguments: `MyValue(value=raw)`.
- Optional constructor metadata: `title` and `parameter` customize validation error context.
- `.value` exposes the stored value.
- `.title` and `.parameter` expose error-context metadata.
- `.type()` returns the declared wrapped type when it can be inferred from `ValueObject[T]`.
- `repr(obj)` defaults to `ClassName(value=<display value>)`.
- `str(obj)` defaults to `str(<display value>)`.
- Equality requires the same concrete class and equal wrapped values.
- Instances reject attribute mutation after construction.
- Shallow and deep copy create equal new instances.

Use `ValueObject[T]` directly when no reusable class already represents the needed rule.

## Validation Hooks

Use `@validation(order=N)` for rejection rules. A validation method receives `value` and returns `None`.

```python
from value_object_pattern import ValueObject, validation


class PositiveQuantity(ValueObject[int]):
    @validation(order=0)
    def _ensure_value_is_integer(self, value: int) -> None:
        if type(value) is not int:
            raise TypeError('PositiveQuantity value must be an integer.')

    @validation(order=1)
    def _ensure_value_is_positive(self, value: int) -> None:
        if value <= 0:
            raise ValueError('PositiveQuantity value must be positive.')
```

Validation methods run in ascending `order`. Methods without an explicit order are ordered by method name. Prefer
explicit order when one validation depends on another.

Reusable validators delegate failures through protected `_raise_*` methods. Override those methods when a domain value
object needs custom exception types or context. Do not override `_validate()` merely to replace reusable exceptions;
that duplicates ordering and can bypass inherited rules.

`@validation(order=N, early_process=True)` passes both `value` and `processed_value` after running processors early. Use
this only when validation must inspect normalized/coerced input before storage.

## Processing Hooks

Use `@process(order=N)` for deterministic normalization. A process method receives the current value and returns the
next value.

```python
from value_object_pattern import process
from value_object_pattern.usables import StringValueObject


class LowerTrimmedName(StringValueObject):
    @process(order=0)
    def _trim(self, value: str) -> str:
        return value.strip()

    @process(order=1)
    def _lower(self, value: str) -> str:
        return value.lower()
```

Processing normally runs after validation. If a validator uses `early_process=True`, processing is run before that
validator and the processed value is cached for storage.

## Choosing A Base Class

- Use `ValueObject[T]` for a new primitive or object-backed domain concept.
- Use a reusable base class such as `StringValueObject`, `NotEmptyStringValueObject`, or `PositiveIntegerValueObject`
  when it already enforces part of the rule.
- Use `EnumerationValueObject[E]` for enum-backed values that should accept enum members or raw enum values.
- Use `UnionValueObject[T]` when the stored value may be one of several annotated types and conversion should try the
  union candidates in order.
- Use `ListValueObject[T]` or `DictValueObject[K, V]` when the collection itself has domain meaning. Both also support
  inline construction as `ListValueObject[T](...)` and `DictValueObject[K, V](...)` for local typed collection
  validation.
- Use `BaseModel` for aggregate-like models with multiple attributes and primitive conversion.

## EnumerationValueObject

`EnumerationValueObject[E]` validates against an `Enum` subclass and stores the enum member. Input can be an enum member
or a raw enum value.

```python
from enum import Enum, unique

from value_object_pattern import EnumerationValueObject


@unique
class OrderStatus(Enum):
    DRAFT = 'draft'
    PAID = 'paid'


class OrderStatusValue(EnumerationValueObject[OrderStatus]):
    pass


assert OrderStatusValue(value='paid').value is OrderStatus.PAID
```

Parameterize the subclass. Unparameterized subclasses raise at class creation.

## UnionValueObject

`UnionValueObject[T]` stores the first union candidate that can represent the input. It supports primitives,
`ValueObject` subclasses, `BaseModel` subclasses, enums, nested collections, and unions. Use a named subclass for
reusable domain concepts, or construct `UnionValueObject[T]` inline for local conversion.

```python
from value_object_pattern import UnionValueObject
from value_object_pattern.usables import PositiveIntegerValueObject


class IdOrSlug(UnionValueObject[PositiveIntegerValueObject | str]):
    pass


assert isinstance(IdOrSlug(value=10).value, PositiveIntegerValueObject)
assert IdOrSlug(value='tenant-a').value == 'tenant-a'
assert isinstance(UnionValueObject[PositiveIntegerValueObject | str](value=10).value, PositiveIntegerValueObject)
```

Candidate order matters. Put more specific or richer candidates before broader primitives when both could match.
When no candidate matches, named subclasses can override `_raise_value_is_not_of_type()` to raise a domain-specific
error.

## Display Overrides

Override `_value_for_display()` only when display/primitive output should differ from the stored value. The package uses
this pattern for `SecretStringValueObject`, which redacts display output. Redaction is not encryption.

```python
from value_object_pattern.usables import SecretStringValueObject


token = SecretStringValueObject(value='secret')
assert str(token) == '********'
```

## Error Context

Reusable validators can report domain-specific names through `title` and `parameter`.

```python
from value_object_pattern.usables import NotEmptyStringValueObject


NotEmptyStringValueObject(value='Ada', title='User', parameter='name')
```

When validation fails, the error message uses the supplied context instead of the reusable class name and default
`value` parameter.
