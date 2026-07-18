---
name: value-object-pattern
description: Use this skill when working in Python projects that use or should use the value-object-pattern package. Use it for domain primitives, value objects, validation wrappers, DDD-style typed values, reusable validators, primitive conversion, BaseModel aggregates, ListValueObject, DictValueObject, EnumerationValueObject, UnionValueObject, or when replacing scattered validation with named immutable objects, even if the user only says "make this field validated" or "avoid primitive obsession."
license: MIT
compatibility: Designed for Agent Skills-compatible coding agents. Python project guidance is authored from value-object-pattern 1.31.0 and Python 3.11+; verify the consuming project's pinned package version before relying on newer APIs.
metadata:
  package: value-object-pattern
  package-version: '1.31.0'
  source: https://github.com/adriamontoto/value-object-pattern
---

# Value Object Pattern

Use this skill to help users apply the `value-object-pattern` Python package in their own projects. The package creates
immutable, self-validating value objects and reusable validation primitives.

## First Steps

1. Inspect the consuming project before editing:
   - Check dependency files for `value-object-pattern` and its pinned version.
   - Check existing domain model, validation, and test conventions.
   - If the package is absent and the task requires it, propose adding `value-object-pattern` instead of inventing a
     local framework.
2. Decide whether a value object is warranted:
   - Use a value object when a primitive has a named domain meaning or reusable rule.
   - Keep raw primitives for exact literals, boundary examples, low-level calculations, and third-party API calls.
   - Use `.value` at storage, serialization, HTTP, CLI, and library boundaries.
3. Prefer reusable value objects before writing custom classes.
4. For custom rules, subclass `ValueObject[T]` or the closest reusable base class.
5. Add focused tests for valid construction, invalid construction, normalization, primitive conversion, and display.
6. When a reusable validator exposes a protected `_raise_*` hook, override that hook for domain-specific exceptions;
   do not replace `_validate()` or duplicate the inherited validation pipeline.

## What To Load

- Read [references/core-api.md](references/core-api.md) when creating custom value objects, enum-backed values, unions,
  or ordered validation/processing hooks.
- Read [references/conversion-and-modeling.md](references/conversion-and-modeling.md) when modeling aggregates,
  serializing/deserializing, using `BaseModel`, or working with typed list/dict value objects.
- Read [references/reusable-catalog.md](references/reusable-catalog.md) when choosing built-in validators or imports.
- Read [references/examples-and-testing.md](references/examples-and-testing.md) when writing examples, tests, or review
  guidance.

## Default Implementation Pattern

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

If a reusable base already exists, subclass it and add only the missing domain rule:

```python
from value_object_pattern import validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class TenantName(NotEmptyStringValueObject, TrimmedStringValueObject):
    @validation(order=0)
    def _ensure_value_has_allowed_length(self, value: str) -> None:
        if len(value) > 80:
            raise ValueError('TenantName value must contain at most 80 characters.')
```

## Review Checklist

- The value object name describes the domain concept, not only the primitive type.
- Constructor calls use keyword arguments: `EmailAddressValueObject(value='ada@example.com')`.
- Validation hooks reject invalid data; processing hooks perform deterministic normalization.
- Domain-specific exceptions override reusable `_raise_*` hooks instead of validators.
- Hook order is explicit when order matters.
- Tests assert `.value`, normalization, expected failures, and boundary conversion.
- `BaseModel.from_primitives()` is backed by constructor annotations.
- `SecretStringValueObject` is treated as display redaction, not encryption or secure storage.
- Public API imports are stable for the consuming project; if in doubt, use documented package paths.

## Common Mistakes

- Do not scatter the same validation rule across services after creating a value object.
- Do not compare a value object directly with a raw primitive unless the project has intentionally added that behavior.
- Do not mutate value objects; create a new instance or use collection helpers that return a new instance.
- Do not call `.value` too early inside domain logic. Keep rich types until crossing a primitive-only boundary.
- Do not use current time implicitly in tests for date/datetime helpers. Pass explicit reference dates or datetimes.

## When Editing This Repository

Follow the repository `AGENTS.md`: inspect before modifying, preserve local style, update nearby tests and exports, and
run the relevant Make targets. If public value-object APIs, reusable catalog entries, primitive conversion behavior, or
documented package-version facts change, update this skill and regenerate the `.skill` package.
