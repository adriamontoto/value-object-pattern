# Primitive Value Objects

Primitive value objects wrap common Python scalar types and apply focused validation rules. Use these classes when the
domain rule is generic enough to be shared across projects.

## Imports

Most primitive value objects are re-exported from `value_object_pattern.usables`:

```python
from value_object_pattern.usables import NotEmptyStringValueObject, PositiveIntegerValueObject
```

Category-specific imports are also available:

```python
from value_object_pattern.usables.primitives.string import SnakeCaseStringValueObject
from value_object_pattern.usables.primitives.integer import EvenIntegerValueObject
```

## Strings

| Value Object | Rule |
| --- | --- |
| `StringValueObject` | Accepts only exact `str` values. |
| `NotEmptyStringValueObject` | Rejects empty strings. |
| `TrimmedStringValueObject` | Rejects values with leading or trailing whitespace. |
| `SecretStringValueObject` | Stores a string and redacts display through `repr()` and `str()`. |
| `AlphaStringValueObject` | Accepts alphabetic strings. |
| `AlphanumericStringValueObject` | Accepts alphabetic and numeric characters. |
| `DigitStringValueObject` | Accepts digit-only strings. |
| `PrintableStringValueObject` | Accepts printable strings. |
| `LowercaseStringValueObject` | Accepts lowercase strings. |
| `UppercaseStringValueObject` | Accepts uppercase strings. |
| `SnakeCaseStringValueObject` | Accepts snake_case strings. |
| `ScreamingSnakeCaseStringValueObject` | Accepts SCREAMING_SNAKE_CASE strings. |
| `KebabCaseStringValueObject` | Accepts kebab-case strings. |
| `CamelCaseStringValueObject` | Accepts camelCase strings. |
| `PascalCaseStringValueObject` | Accepts PascalCase strings. |

## Numbers, Booleans, Bytes, And None

| Value Object | Rule |
| --- | --- |
| `IntegerValueObject` | Accepts only exact `int` values. |
| `PositiveIntegerValueObject` | Accepts integers greater than zero. |
| `PositiveOrZeroIntegerValueObject` | Accepts integers greater than or equal to zero. |
| `NegativeIntegerValueObject` | Accepts integers lower than zero. |
| `NegativeOrZeroIntegerValueObject` | Accepts integers lower than or equal to zero. |
| `EvenIntegerValueObject` | Accepts even integers. |
| `OddIntegerValueObject` | Accepts odd integers. |
| `FloatValueObject` | Accepts only exact `float` values. |
| `PositiveFloatValueObject` | Accepts floats greater than zero. |
| `PositiveOrZeroFloatValueObject` | Accepts floats greater than or equal to zero. |
| `NegativeFloatValueObject` | Accepts floats lower than zero. |
| `NegativeOrZeroFloatValueObject` | Accepts floats lower than or equal to zero. |
| `BooleanValueObject` | Accepts only exact `bool` values. |
| `TrueValueObject` | Accepts only `True`. |
| `FalseValueObject` | Accepts only `False`. |
| `BytesValueObject` | Accepts only exact `bytes` values. |
| `NoneValueObject` | Accepts only `None`. |
| `NotNoneValueObject` | Rejects `None`. |

## Example

```python
from value_object_pattern.usables import PositiveIntegerValueObject, SnakeCaseStringValueObject

limit = PositiveIntegerValueObject(value=25)
key = SnakeCaseStringValueObject(value='page_size')

assert limit.value == 25
assert key.value == 'page_size'
```

## Selection Notes

- Use primitive value objects for reusable shape rules, not business-specific policy.
- Use `SecretStringValueObject` for display redaction only; it does not encrypt or hash the stored value.
- Prefer custom subclasses when the name should explain a domain concept such as `UserName`, `RetryLimit`, or
  `TenantSlug`.
