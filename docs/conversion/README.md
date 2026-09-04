# Primitive Conversion

Value Object Pattern includes recursive conversion helpers for moving between primitives and richer value-object/model
types. This is useful at API, persistence, messaging, and test boundaries.

## To Primitives

`to_primitives()` converts public model state recursively:

```python
from value_object_pattern import BaseModel
from value_object_pattern.usables import NotEmptyStringValueObject


class User(BaseModel):
    def __init__(self, name: NotEmptyStringValueObject) -> None:
        self.name = name


user = User(name=NotEmptyStringValueObject(value='Ada'))

assert user.to_primitives() == {'name': 'Ada'}
```

When nested in a model or typed collection, value objects convert through their stored value and enums convert through
their member value. A value object composed with `SecretValueObject` redacts `str()` and `repr()` without changing
primitive conversion.

## From Primitives

`from_primitives()` uses constructor annotations to build nested values:

```python
from value_object_pattern import BaseModel
from value_object_pattern.usables import NotEmptyStringValueObject, PositiveIntegerValueObject


class User(BaseModel):
    def __init__(self, name: NotEmptyStringValueObject, age: PositiveIntegerValueObject) -> None:
        self.name = name
        self.age = age


user = User.from_primitives(primitives={'name': 'Ada', 'age': 42})

assert isinstance(user.name, NotEmptyStringValueObject)
assert isinstance(user.age, PositiveIntegerValueObject)
```

## Collections

Typed collection constructors accept primitive items, already-created typed items, or a mixture of both. Use a named
subclass when the collection has domain meaning, or construct an inline collection for local typed-collection
validation. `from_primitives()` remains available when an explicit boundary-conversion name is clearer:

Collection updates are immutable: list positional helpers return new instances, and dictionary `merge()` converts and
combines multiple typed or primitive entries into a new instance.

| Class                      | Accepted outer input                | `to_primitives()` outer type |
| -------------------------- | ----------------------------------- | ---------------------------- |
| `ListValueObject[T]`       | `list`                              | `list`                       |
| `DictValueObject[K, V]`    | `dict`                              | `dict`                       |
| `SequenceValueObject[T]`   | Non-text sequence                   | `tuple`                      |
| `TupleValueObject[T]`      | `tuple`                             | `tuple`                      |
| `MappingValueObject[K, V]` | Mapping                             | `dict`                       |
| `SetValueObject[T]`        | `set`                               | `set`                        |
| `FrozenSetValueObject[T]`  | `frozenset`                         | `frozenset`                  |

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
from value_object_pattern.usables import PositiveIntegerValueObject


class Quantities(ListValueObject[PositiveIntegerValueObject]):
    pass


three = PositiveIntegerValueObject(value=3)
values = Quantities(value=[1, 2, three]).add(item=4)
inline_values = ListValueObject[PositiveIntegerValueObject](value=[1, 2, three])
inline_stock = DictValueObject[str, PositiveIntegerValueObject](value={'sku-1': 10})
sequence = SequenceValueObject[PositiveIntegerValueObject](value=[1, 2])
tuple_value = TupleValueObject[PositiveIntegerValueObject](value=(1, 2))
mapping = MappingValueObject[str, PositiveIntegerValueObject](value={'sku-1': 10})
set_value = SetValueObject[PositiveIntegerValueObject](value={1, 2})
frozen = FrozenSetValueObject[PositiveIntegerValueObject](value=frozenset({1, 2}))

assert values.to_primitives() == [1, 2, 3, 4]
assert inline_values.to_primitives() == [1, 2, 3]
assert inline_stock.to_primitives() == {'sku-1': 10}
assert sequence.to_primitives() == (1, 2)
assert tuple_value.to_primitives() == (1, 2)
assert mapping.to_primitives() == {'sku-1': 10}
assert set_value.to_primitives() == {1, 2}
assert frozen.to_primitives() == frozenset({1, 2})
```

Mapping and sequence protocol wrappers snapshot their inputs. Concrete list, dictionary, tuple, set, and frozen-set
wrappers require the matching outer type. All update helpers return a new wrapper, and set operators preserve the
wrapper class.

## Unions

`UnionValueObject` tries union candidates in order and stores the first matching converted value. You can use a named
subclass when the union has domain meaning, or construct an inline union for local conversion:

```python
from value_object_pattern import UnionValueObject
from value_object_pattern.usables import PositiveIntegerValueObject


class IdOrName(UnionValueObject[PositiveIntegerValueObject | str]):
    pass


identifier = IdOrName(value=7)
name = IdOrName(value='Ada')
inline_identifier = UnionValueObject[PositiveIntegerValueObject | str](value=7)

assert isinstance(identifier.value, PositiveIntegerValueObject)
assert name.value == 'Ada'
assert isinstance(inline_identifier.value, PositiveIntegerValueObject)
```

## Conversion Checklist

- Add constructor annotations to `BaseModel` subclasses if you want `from_primitives()` to build rich types.
- Use primitive conversion at boundaries, not in the middle of domain logic.
- Treat `to_primitives()` output as display/API data, not necessarily secret-safe storage.
- Use explicit tests for nested model, collection, enum, and union conversion paths.
