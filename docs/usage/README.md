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

```python
from value_object_pattern.models.collections import ListValueObject
from value_object_pattern.usables import PositiveIntegerValueObject


class Quantities(ListValueObject[PositiveIntegerValueObject]):
    pass


quantities = Quantities(value=[PositiveIntegerValueObject(value=1)])
updated = quantities.add_from_primitives(item=2)

assert updated.to_primitives() == [1, 2]
```

Collection helpers return new value-object instances rather than mutating the original object.

## Usage Checklist

- Put domain rules in value objects instead of scattering validation across services.
- Use `@validation` for rejection rules.
- Use `@process` for normalization rules.
- Keep value objects small and focused on one wrapped value.
- Use `BaseModel` when you need nested primitive conversion.
- Prefer reusable value objects when the package already provides the needed constraint.

