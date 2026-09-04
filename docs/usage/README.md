# Usage Guide

Value objects are small immutable wrappers that validate and optionally normalize a single value. They are useful when a
plain primitive is too permissive for the domain rule.

## Define A Value Object

```python
from value_object_pattern import ValueObject, validation


class Age(ValueObject[int]):
    @validation(order=0)
    def _ensure_value_is_integer(self, value: int) -> None:
        if type(value) is not int:
            raise TypeError('Age value must be an integer.')

    @validation(order=1)
    def _ensure_value_is_positive(self, value: int) -> None:
        if value <= 0:
            raise ValueError('Age value must be positive.')
```

Construction validates immediately:

```python
age = Age(value=42)

assert age.value == 42
```

## Normalize With `@process`

Use `@process` for deterministic transformations:

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


assert LowerTrimmedName(value='  ADA  ').value == 'ada'
```

Processing runs after validation unless a validator opts into early processing.

## Customize Error Context

`title` and `parameter` make reusable validators report domain-specific errors:

```python
from value_object_pattern.usables import NotEmptyStringValueObject

name = NotEmptyStringValueObject(value='Ada', title='User', parameter='name')
```

If validation fails, the error message uses `User name` instead of the reusable class name and default `value`
parameter.

## Use BaseModel For Aggregates

`BaseModel` helps convert nested value objects to and from primitives:

```python
from value_object_pattern import BaseModel
from value_object_pattern.usables import NotEmptyStringValueObject, PositiveIntegerValueObject


class User(BaseModel):
    def __init__(self, name: NotEmptyStringValueObject, age: PositiveIntegerValueObject) -> None:
        self.name = name
        self.age = age


user = User.from_primitives(primitives={'name': 'Ada', 'age': 42})

assert user.to_primitives() == {'age': 42, 'name': 'Ada'}
```

Double-underscore private attributes are omitted from public representation and primitive output.

## Use Collection Value Objects

Choose the collection by the outer input contract and canonical exposed value:

| Class                      | Accepted outer input                     | Canonical `.value`                         |
| -------------------------- | ---------------------------------------- | ------------------------------------------ |
| `ListValueObject[T]`       | Exact `list`                             | Defensive `list[T]` copy                   |
| `DictValueObject[K, V]`    | Exact `dict`                             | Defensive `dict[K, V]` copy                |
| `SequenceValueObject[T]`   | Non-text `collections.abc.Sequence`      | `tuple[T, ...]`                            |
| `TupleValueObject[T]`      | Exact `tuple`                            | `tuple[T, ...]`                            |
| `MappingValueObject[K, V]` | Any `collections.abc.Mapping`            | Read-only mapping over a defensive snapshot |
| `SetValueObject[T]`        | Exact `set`                              | Defensive `set[T]` copy                    |
| `FrozenSetValueObject[T]`  | Exact `frozenset`                        | `frozenset[T]`                             |

Each collection supports a named subclass for a domain concept and inline construction for local validation.

```python
from value_object_pattern.models.collections import (
    DictValueObject,
    FrozenSetValueObject,
    ListValueObject,
    MappingValueObject,
    SequenceValueObject,
    SetValueObject,
    TupleValueObject,
)


class Quantities(ListValueObject[int]):
    pass


class StockBySku(DictValueObject[str, int]):
    pass


quantities = Quantities(value=[1, 2])
updated_quantities = quantities.add(item=3)
stock = StockBySku(value={'sku-1': 10}).set(key='sku-2', value=5)
sequence = SequenceValueObject[int](value=range(3))
tuple_value = TupleValueObject[int](value=(1, 2))
read_only_stock = MappingValueObject[str, int](value={'sku-1': 10})
tags = SetValueObject[str](value={'python'}).add(item='typing')
frozen_tags = FrozenSetValueObject[str](value=frozenset({'python'})).add(item='typing')

assert quantities.value == [1, 2]
assert updated_quantities.to_primitives() == [1, 2, 3]
assert stock.to_primitives() == {'sku-1': 10, 'sku-2': 5}
assert sequence.value == (0, 1, 2)
assert tuple_value.value == (1, 2)
assert dict(read_only_stock.value) == {'sku-1': 10}
assert tags.value == {'python', 'typing'}
assert frozen_tags.value == frozenset({'python', 'typing'})
```

Collection constructors and update helpers accept primitive items, already-created typed items, or a mixture of both.
Helpers return new value-object instances rather than mutating the original object. `ListValueObject`,
`DictValueObject`, `TupleValueObject`, `SetValueObject`, and `FrozenSetValueObject` require their concrete outer
collection type. `SequenceValueObject` accepts non-scalar sequences and normalizes them to tuples, while
`MappingValueObject` accepts any mapping and exposes a read-only snapshot. Collection inputs and `.value` use shallow
defensive boundaries, and set wrappers provide persistent set algebra.

List and sequence wrappers provide `add`, `extend`, `insert`, `replace`, `remove_at`, `delete`, and `delete_all`.
Dictionary and mapping wrappers provide `get`, `set`, `merge`, and `delete`. Set wrappers provide `add`, `update`,
`remove`, `discard`, union, intersection, difference, symmetric difference, and subset/superset comparisons.

### Customize Collection Exceptions

Every error raised under a collection value object's control is routed through a protected `_raise_*` hook. Override
the relevant hook in a named subclass to replace the exception type or message while keeping validation and collection
operations unchanged.

```python
from typing import Any, NoReturn

from value_object_pattern.models.collections import ListValueObject


class InvalidQuantityError(TypeError):
    pass


class Quantities(ListValueObject[int]):
    def _raise_value_is_not_of_type(self, value: Any) -> NoReturn:
        raise InvalidQuantityError(f'invalid quantity: {value}')
```

Generic parameterization errors use class-level hooks such as `_raise_missing_type_arguments()`,
`_raise_invalid_type_argument_count()`, and `_raise_type_argument_is_not_type()`. Instance validation and operation
hooks cover outer collection types, key/item/value types, missing keys or items, indexes, tuple input, and set operands.
Default hooks retain the standard exception classes and messages. Errors produced outside the wrapper's control, such
as mutating the read-only `mappingproxy` returned by `MappingValueObject.value`, remain native Python errors.

## Usage Checklist

- Put domain rules in value objects instead of scattering validation across services.
- Use `@validation` for rejection rules.
- Use `@process` for normalization rules.
- Keep value objects small and focused on one wrapped value.
- Use `BaseModel` when you need nested primitive conversion.
- Prefer reusable value objects when the package already provides the needed constraint.
