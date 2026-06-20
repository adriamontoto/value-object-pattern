# Conversion And Modeling Reference

Use this file when working with models, primitive conversion, list value objects, or dictionary value objects.

## BaseModel

`BaseModel` is for aggregate-like domain models that contain value objects, enums, primitives, collections, or nested
models. Public and single-underscore attributes participate in representation, equality, hashing, and primitive
conversion. Double-underscore private attributes are omitted from public representation and `to_primitives()`.

```python
from value_object_pattern import BaseModel
from value_object_pattern.usables import NotEmptyStringValueObject, PositiveIntegerValueObject


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

`ListValueObject[T]` validates that the wrapped value is a list and each item matches the declared item type. Helpers
return new instances rather than mutating the original object. Use a named subclass for domain collections, or construct
`ListValueObject[T]` inline for local typed-list validation.

Supported read behavior:

- `item in collection`
- iteration
- `len(collection)`
- `reversed(collection)`
- `is_empty()`
- `repr()` / `str()`

Supported update helpers:

- `add(item=...)`
- `add_from_primitives(item=...)`
- `extend(items=[...])`
- `extend_from_primitives(items=[...])`
- `delete(item=...)`
- `delete_from_primitives(item=...)`
- `delete_all(items=[...])`
- `delete_all_from_primitives(items=[...])`
- `from_primitives(value=[...])`
- `to_primitives()`

```python
from value_object_pattern.models.collections import ListValueObject
from value_object_pattern.usables import PositiveIntegerValueObject


class Quantities(ListValueObject[PositiveIntegerValueObject]):
    pass


quantities = Quantities.from_primitives(value=[1, 2])
updated = quantities.add_from_primitives(item=3)
inline_quantities = ListValueObject[PositiveIntegerValueObject].from_primitives(value=[1, 2, 3])

assert quantities.to_primitives() == [1, 2]
assert updated.to_primitives() == [1, 2, 3]
assert inline_quantities.to_primitives() == [1, 2, 3]
```

## DictValueObject

`DictValueObject[K, V]` validates that the wrapped value is a dictionary and validates each key/value against the
declared types. Use a named subclass for domain mappings, or construct `DictValueObject[K, V]` inline for local typed
dictionary validation.

Supported read behavior:

- `key in mapping`
- iteration over keys
- `reversed(mapping)`
- `len(mapping)`
- `mapping[key]`
- `get(key=..., default=...)`
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

## Conversion Rules To Remember

- `BaseModel.from_primitives(primitives={...})` expects constructor parameter names, not arbitrary object attributes.
- Extra or missing constructor parameters are rejected.
- Collection `.from_primitives()` methods use `value=...`, while `BaseModel.from_primitives()` uses `primitives=...`.
- `ListValueObject` can be constructed inline as `ListValueObject[T](...)`.
- `DictValueObject` can be constructed inline as `DictValueObject[K, V](...)`.
- `UnionValueObject` tries candidates in annotation order and can be constructed inline as `UnionValueObject[T](...)`.
- `SecretStringValueObject` converts through its display value, so `to_primitives()` may produce a masked string.
- Keep raw primitive conversion near I/O; avoid unpacking `.value` throughout domain code.
