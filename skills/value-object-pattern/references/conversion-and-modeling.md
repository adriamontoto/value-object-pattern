# Conversion And Modeling Reference

Use this file when working with models, primitive conversion, or typed collection value objects.

## BaseModel

`BaseModel` is for aggregate-like domain models that contain value objects, enums, primitives, collections, or nested
models. Public and single-underscore attributes participate in representation, equality, hashing, and primitive
conversion. Double-underscore private attributes are omitted from public representation and `to_primitives()`.

```python
from value_object_pattern import BaseModel
from value_object_pattern.usables import (
    NotEmptyStringValueObject,
    PositiveIntegerValueObject,
)


class User(BaseModel):
    def __init__(self, name: NotEmptyStringValueObject, age: PositiveIntegerValueObject) -> None:
        self.name = name
        self.age = age


user = User.from_primitives(primitives={'name': 'Ada', 'age': 42})

assert isinstance(user.name, NotEmptyStringValueObject)
assert user.to_primitives() == {'age': 42, 'name': 'Ada'}
```

`from_primitives()` uses constructor annotations. If annotations are missing or too broad, conversion cannot reliably
build nested value objects.

## Primitive Boundaries

Use rich value objects inside domain logic and convert at boundaries:

- HTTP request/response payloads
- CLI arguments
- persistence rows/documents
- message queues
- JSON/YAML/TOML config
- third-party libraries that require primitives

Prefer `BaseModel.from_primitives()` at inbound boundaries and `to_primitives()` at outbound boundaries.

## ListValueObject

`ListValueObject[T]` validates that the wrapped value is a list and each item matches the declared item type. The input
list and `.value` are shallow-copied at the collection boundary, so top-level collection mutations cannot bypass
validation; nested items are not deep-copied. Helpers return new instances rather than mutating the original object.
Use a named subclass for domain collections, or construct `ListValueObject[T]` inline for local typed-list validation.

`from_primitives()` validates that its input is a list before converting items. Named subclasses can override
`_raise_value_is_not_list()` to provide a domain-specific container error.

Membership converts primitive items through the declared item type, and indexing follows normal list integer and slice
semantics while returning the stored typed items.

Supported behavior:

- `item in collection`
- `primitive_item in collection`
- iteration
- `len(collection)`
- `reversed(collection)`
- `collection[index]` or `collection[start:stop]`
- `collection.count(item)`
- `collection.index(item, start=..., stop=...)`
- `is_empty()`
- `repr()` / `str()`

Supported update helpers:

- `add(item=...)`
- `extend(items=[...])`
- `insert(index, item)`
- `replace(index, item)`
- `remove_at(index)`
- `delete(item=...)`
- `delete_all(items=[...])`
- `from_primitives(value=[...])`
- `to_primitives()`

The update helpers accept typed or primitive items and convert them through the declared item type automatically.

```python
from value_object_pattern.models.collections import ListValueObject
from value_object_pattern.usables import PositiveIntegerValueObject


class Quantities(ListValueObject[PositiveIntegerValueObject]):
    pass


quantities = Quantities.from_primitives(value=[1, 2])
updated = quantities.add(item=3)
inline_quantities = ListValueObject[PositiveIntegerValueObject].from_primitives(value=[1, 2, 3])

assert quantities.to_primitives() == [1, 2]
assert updated.to_primitives() == [1, 2, 3]
assert inline_quantities.to_primitives() == [1, 2, 3]
```

## DictValueObject

`DictValueObject[K, V]` validates that the wrapped value is a dictionary and validates each key/value against the
declared types. The input dictionary and `.value` are shallow-copied at the collection boundary, so top-level
collection mutations cannot bypass validation; nested values are not deep-copied. Use a named subclass for domain
mappings, or construct `DictValueObject[K, V]` inline for local typed dictionary validation.

`from_primitives()` validates that its input is a dictionary before converting keys and values. Named subclasses can
override `_raise_not_is_not_dict()` to provide a domain-specific container error.

Dictionary lookups and updates convert primitive keys through the declared key type. `set(key=..., value=...)` also
converts primitive values, replaces existing keys, and returns a new mapping. `merge(values=...)` converts and merges
multiple primitive or typed entries. `delete(key=...)` returns a new mapping without the key and raises `KeyError` when
the key is missing.

Supported behavior:

- `key in mapping`
- iteration over keys
- `reversed(mapping)`
- `len(mapping)`
- `mapping[key]` or `mapping[primitive_key]`
- `get(key=..., default=...)`
- `set(key=..., value=...)`
- `merge(values=...)`
- `delete(key=...)`
- `items()`
- `keys()`
- `values()`
- `is_empty()`
- `from_primitives(value={...})`
- `to_primitives()`

```python
from value_object_pattern.models.collections import DictValueObject
from value_object_pattern.usables import PositiveIntegerValueObject


class StockBySku(DictValueObject[str, PositiveIntegerValueObject]):
    pass


stock = StockBySku.from_primitives(value={'sku-1': 10})
inline_stock = DictValueObject[str, PositiveIntegerValueObject].from_primitives(value={'sku-1': 10})

assert stock['sku-1'].value == 10
assert stock.to_primitives() == {'sku-1': 10}
assert inline_stock.to_primitives() == {'sku-1': 10}
```

## Additional Collection Value Objects

All collection classes support named subclasses, inline construction, typed contents, persistent update helpers, and
recursive primitive conversion. Each class remains in its own module. `TupleValueObject` specializes the shared
sequence contract, while `SetValueObject` and `FrozenSetValueObject` share a private set implementation; these internal
relationships do not change their accepted outer values or canonical public values.

| Class                      | Accepted outer value                    | Canonical `.value`         |
| -------------------------- | --------------------------------------- | -------------------------- |
| `SequenceValueObject[T]`   | Any non-text `collections.abc.Sequence` | `tuple[T, ...]`            |
| `TupleValueObject[T]`      | `tuple`                                 | `tuple[T, ...]`            |
| `MappingValueObject[K, V]` | Any `collections.abc.Mapping`           | Read-only mapping snapshot |
| `SetValueObject[T]`        | `set`                                   | Defensive `set[T]` copy    |
| `FrozenSetValueObject[T]`  | `frozenset`                             | `frozenset[T]`             |

Sequence wrappers provide indexing and immutable positional updates. Mapping wrappers provide lookup, `set()`,
`merge()`, and `delete()`. Set wrappers provide persistent `add()`, `update()`, `remove()`, and `discard()`, plus native
set algebra methods and operators.

```python
from value_object_pattern.models.collections import (
    MappingValueObject,
    SequenceValueObject,
    SetValueObject,
)
from value_object_pattern.usables import PositiveIntegerValueObject

sequence = SequenceValueObject[PositiveIntegerValueObject].from_primitives(value=[1, 2])
mapping = MappingValueObject[str, PositiveIntegerValueObject].from_primitives(value={'sku-1': 10})
tags = SetValueObject[str](value={'python'}) | {'typing'}

assert sequence.to_primitives() == (1, 2)
assert mapping.to_primitives() == {'sku-1': 10}
assert tags.value == {'python', 'typing'}
```

### Custom collection exceptions

Collection-controlled failures delegate to protected `_raise_*` hooks. A named subclass can override a hook to replace
the exception without replacing the validator or persistent collection operation:

```python
from typing import Any, NoReturn

from value_object_pattern.models.collections import ListValueObject


class InvalidQuantityError(TypeError):
    pass


class Quantities(ListValueObject[int]):
    def _raise_value_is_not_of_type(self, value: Any) -> NoReturn:
        raise InvalidQuantityError(f'invalid quantity: {value}')
```

Parameterization hooks are class methods: `_raise_missing_type_arguments()`,
`_raise_invalid_type_argument_count()` where the collection has an argument-count constraint, and
`_raise_type_argument_is_not_type()`. Instance hooks cover outer-type validation, item/key/value validation, missing
keys or items, indexes, tuple input, and set operands. Default implementations preserve the package's normal exception
types and messages. Native behavior outside a wrapper operation, including `mappingproxy` mutation, is not intercepted.

## Conversion Rules To Remember

- `BaseModel.from_primitives(primitives={...})` expects constructor parameter names, not arbitrary object attributes.
- Extra or missing constructor parameters are rejected.
- Collection `.from_primitives()` methods use `value=...`, while `BaseModel.from_primitives()` uses `primitives=...`.
- `ListValueObject` can be constructed inline as `ListValueObject[T](...)`.
- `DictValueObject` can be constructed inline as `DictValueObject[K, V](...)`.
- Sequence, tuple, set, and frozen-set wrappers use one item type; mapping wrappers use key and value types.
- `SequenceValueObject` rejects text and binary scalar sequences and normalizes accepted input to a tuple.
- `MappingValueObject` snapshots arbitrary mappings and exposes a read-only mapping value.
- `UnionValueObject` tries candidates in annotation order and can be constructed inline as `UnionValueObject[T](...)`.
- A value object composed with `SecretValueObject` redacts `str()` and `repr()` in either inheritance order while raw
  primitive conversion returns the stored value.
- Keep raw primitive conversion near I/O; avoid unpacking `.value` throughout domain code.
