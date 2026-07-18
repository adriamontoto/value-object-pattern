# Secret Value Object Composition Design

## Goal

Make `SecretValueObject` a composition-only display-redaction marker that can be combined with every `ValueObject`
subclass without repeating or knowing the wrapped type and without depending on base-class order.

Both declarations must behave identically:

```python
class SecretDictionary(SecretValueObject, DictValueObject[str, str]):
    pass


class AnotherSecretDictionary(DictValueObject[str, str], SecretValueObject):
    pass
```

## Public API

`SecretValueObject` becomes a non-generic marker and cannot be used as a standalone value object. The accompanying
value-object base remains responsible for construction, typing, validation, processing, equality, hashing, and primitive
conversion.

The old `SecretValueObject[T]` syntax is removed. `SecretStringValueObject` is also removed from its module and every
public export. String secrets use composition in the same way as every other type:

```python
class SecretString(SecretValueObject, StringValueObject):
    pass
```

This is an intentional breaking API change approved for this feature.

## Display Architecture

`SecretValueObject` supplies a marker and the default fixed mask, `********`. It does not implement value storage or
validation.

The `ValueObject` display pipeline resolves the final display value centrally. When an instance carries the secret
marker, the resolver returns its mask before consulting its normal display hook. Central resolution makes redaction
independent of inheritance order and gives redaction precedence over any custom `_value_for_display()` implementation.

Every display-oriented path must use that resolver:

- direct `ValueObject.__str__()` and `ValueObject.__repr__()`;
- recursive display conversion used by models and collections;
- collection value-object display code that renders nested value objects.

Raw `.value` access and `to_primitives()` continue returning the unredacted stored value. Redaction remains a presentation
guard, not encryption or secure storage. Composite classes may override `_MASK` intentionally.

## Supported Composition

The behavior applies uniformly to scalar, collection, and custom value objects. Representative acceptance coverage
includes strings, integers, booleans, lists, and dictionaries, with `SecretValueObject` both before and after the typed
value-object base. Because the redaction decision lives in the shared `ValueObject` display pipeline, the behavior also
applies to other existing and future `ValueObject` subclasses without type-specific secret implementations.

## Validation And Typing

The non-secret base supplies the complete wrapped type, so strict static typing remains intact. For example,
`DictValueObject[str, str]` continues exposing `dict[str, str]`; no secret generic argument degrades `.value` to `Any`.

All existing validators and processors must still run. Adding `SecretValueObject` changes display behavior only and must
not make invalid values acceptable.

## Tests

Tests will replace the `SecretStringValueObject`-specific suite with composition tests that verify:

- direct `str()` and `repr()` use the fixed mask;
- inheritance order does not change redaction, typing, validation, or processing;
- string, integer, boolean, list, dictionary, and custom value-object compositions redact consistently;
- nested model and collection display paths do not expose raw values;
- `.value` and `to_primitives()` preserve raw values;
- custom masks work;
- invalid values still raise the expected exception with an exact `match=` expression.

Object Mothers generate valid and invalid fixtures where only type or shape matters. Explicit mother values are used for
exact display and error-message assertions so those tests remain deterministic.

## Documentation And Migration

The root README, catalog documentation, and installable `skills/value-object-pattern/` references will describe
`SecretValueObject` as a non-generic composition marker. All `SecretStringValueObject` and `SecretValueObject[T]`
examples and catalog entries will be removed or replaced.

Migration examples:

```python
# Before
class SecretPayload(SecretValueObject[dict[str, str]], DictValueObject[str, str]):
    pass


# After
class SecretPayload(SecretValueObject, DictValueObject[str, str]):
    pass
```

```python
# Before
token = SecretStringValueObject(value='hidden')


# After
class SecretToken(SecretValueObject, StringValueObject):
    pass


token = SecretToken(value='hidden')
```

## Verification

Run the repository workflow after implementation:

```bash
make format
make lint
make test
make coverage
```

Coverage is a secondary check; the acceptance matrix and failure assertions provide the behavioral regression coverage.
