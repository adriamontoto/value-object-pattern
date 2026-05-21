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

Value objects convert through their display value. This matters for `SecretStringValueObject`, which returns a masked
display value.

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

Typed collections can convert primitive items into item value objects:

```python
from value_object_pattern.models.collections import ListValueObject
from value_object_pattern.usables import PositiveIntegerValueObject


class Quantities(ListValueObject[PositiveIntegerValueObject]):
    pass


values = Quantities(value=[]).extend_from_primitives(items=[1, 2, 3])

assert values.to_primitives() == [1, 2, 3]
```

## Unions

`UnionValueObject` tries union candidates in order and stores the first matching converted value:

```python
from value_object_pattern import UnionValueObject
from value_object_pattern.usables import PositiveIntegerValueObject


class IdOrName(UnionValueObject[PositiveIntegerValueObject | str]):
    pass


identifier = IdOrName(value=7)
name = IdOrName(value='Ada')

assert isinstance(identifier.value, PositiveIntegerValueObject)
assert name.value == 'Ada'
```

## Conversion Checklist

- Add constructor annotations to `BaseModel` subclasses if you want `from_primitives()` to build rich types.
- Use primitive conversion at boundaries, not in the middle of domain logic.
- Treat `to_primitives()` output as display/API data, not necessarily secret-safe storage.
- Use explicit tests for nested model, collection, enum, and union conversion paths.

