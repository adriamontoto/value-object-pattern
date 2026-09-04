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

| Value Object                                               | Rule                                                           |
| ---------------------------------------------------------- | -------------------------------------------------------------- |
| `StringValueObject`                                        | Accepts only exact `str` values.                               |
| `NotEmptyStringValueObject`                                | Rejects empty strings.                                         |
| `TrimmedStringValueObject`                                 | Rejects values with leading or trailing whitespace.            |
| `HexadecimalStringValueObject` / `Base16StringValueObject` | Accepts valid Base16 strings in either letter case.            |
| `Base32StringValueObject`                                  | Accepts canonical padded Base32 strings in either letter case. |
| `Base36StringValueObject`                                  | Accepts strings from the uppercase Base36 alphabet.            |
| `Base56StringValueObject`                                  | Accepts strings from the ambiguity-free Base56 alphabet.       |
| `Base58StringValueObject`                                  | Accepts strings from the Bitcoin Base58 alphabet.              |
| `Base64StringValueObject`                                  | Accepts canonical standard Base64 strings.                     |
| `AlphaStringValueObject`                                   | Accepts alphabetic strings.                                    |
| `AlphanumericStringValueObject`                            | Accepts alphabetic and numeric characters.                     |
| `DigitStringValueObject`                                   | Accepts digit-only strings.                                    |
| `PrintableStringValueObject`                               | Accepts printable strings.                                     |
| `LowercaseStringValueObject`                               | Accepts lowercase strings.                                     |
| `UppercaseStringValueObject`                               | Accepts uppercase strings.                                     |
| `SnakeCaseStringValueObject`                               | Accepts snake_case strings.                                    |
| `ScreamingSnakeCaseStringValueObject`                      | Accepts SCREAMING_SNAKE_CASE strings.                          |
| `KebabCaseStringValueObject`                               | Accepts kebab-case strings.                                    |
| `CamelCaseStringValueObject`                               | Accepts camelCase strings.                                     |
| `PascalCaseStringValueObject`                              | Accepts PascalCase strings.                                    |

## Numbers, Booleans, Bytes, And None

| Value Object                       | Rule                                            |
| ---------------------------------- | ----------------------------------------------- |
| `IntegerValueObject`               | Accepts only exact `int` values.                |
| `PositiveIntegerValueObject`       | Accepts integers greater than zero.             |
| `PositiveOrZeroIntegerValueObject` | Accepts integers greater than or equal to zero. |
| `NegativeIntegerValueObject`       | Accepts integers lower than zero.               |
| `NegativeOrZeroIntegerValueObject` | Accepts integers lower than or equal to zero.   |
| `EvenIntegerValueObject`           | Accepts even integers.                          |
| `OddIntegerValueObject`            | Accepts odd integers.                           |
| `FloatValueObject`                 | Accepts only exact `float` values.              |
| `NumberValueObject`                | Accepts finite exact `int` or `float` input and stores it as `float`. |
| `PositiveNumberValueObject`        | Accepts finite positive `int` or `float` input and stores it as `float`. |
| `PositiveOrZeroNumberValueObject`  | Accepts finite non-negative `int` or `float` input and stores it as `float`. |
| `PositiveFloatValueObject`         | Accepts floats greater than zero.               |
| `PositiveOrZeroFloatValueObject`   | Accepts floats greater than or equal to zero.   |
| `NegativeFloatValueObject`         | Accepts floats lower than zero.                 |
| `NegativeOrZeroFloatValueObject`   | Accepts floats lower than or equal to zero.     |
| `BooleanValueObject`               | Accepts only exact `bool` values.               |
| `TrueValueObject`                  | Accepts only `True`.                            |
| `FalseValueObject`                 | Accepts only `False`.                           |
| `BytesValueObject`                 | Accepts only exact `bytes` values.              |
| `NoneValueObject`                  | Accepts only `None`.                            |
| `NotNoneValueObject`               | Rejects `None`.                                 |

## Example

```python
from value_object_pattern.usables import (
    NumberValueObject,
    PositiveIntegerValueObject,
    SnakeCaseStringValueObject,
)

limit = PositiveIntegerValueObject(value=25)
ratio = NumberValueObject(value=2)
key = SnakeCaseStringValueObject(value="page_size")

assert limit.value == 25
assert ratio.value == 2.0
assert key.value == "page_size"
```

## Selection Notes

- Use primitive value objects for reusable shape rules, not business-specific policy.
- Compose the root `SecretValueObject` marker with any primitive value object when its display must be redacted. The
  marker works in either inheritance order and does not encrypt or hash the stored value.
- Prefer custom subclasses when the name should explain a domain concept such as `UserName`, `RetryLimit`, or
  `TenantSlug`.
