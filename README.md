<a name="readme-top"></a>

# 📦 Value Object Pattern

<p align="center">
    <a href="https://github.com/adriamontoto/value-object-pattern/actions/workflows/ci.yaml?event=push&branch=master" target="_blank">
        <img src="https://github.com/adriamontoto/value-object-pattern/actions/workflows/ci.yaml/badge.svg?event=push&branch=master" alt="CI Pipeline">
    </a>
        <a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/adriamontoto/value-object-pattern" target="_blank">
        <img src="https://coverage-badge.samuelcolvin.workers.dev/adriamontoto/value-object-pattern.svg" alt="Coverage Pipeline">
    </a>
    <a href="https://pypi.org/project/value-object-pattern" target="_blank">
        <img src="https://img.shields.io/pypi/v/value-object-pattern?color=%2334D058&label=pypi%20package" alt="Package Version">
    </a>
    <a href="https://pypi.org/project/value-object-pattern/" target="_blank">
        <img src="https://img.shields.io/pypi/pyversions/value-object-pattern.svg?color=%2334D058" alt="Supported Python Versions">
    </a>
    <a href="https://pepy.tech/projects/value-object-pattern" target="_blank">
        <img src="https://static.pepy.tech/badge/value-object-pattern/month" alt="Package Downloads">
    </a>
    <a href="https://deepwiki.com/adriamontoto/value-object-pattern" target="_blank">
        <img src="https://img.shields.io/badge/DeepWiki-adriamontoto%2Fvalue--object--pattern-blue.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACwAAAAyCAYAAAAnWDnqAAAAAXNSR0IArs4c6QAAA05JREFUaEPtmUtyEzEQhtWTQyQLHNak2AB7ZnyXZMEjXMGeK/AIi+QuHrMnbChYY7MIh8g01fJoopFb0uhhEqqcbWTp06/uv1saEDv4O3n3dV60RfP947Mm9/SQc0ICFQgzfc4CYZoTPAswgSJCCUJUnAAoRHOAUOcATwbmVLWdGoH//PB8mnKqScAhsD0kYP3j/Yt5LPQe2KvcXmGvRHcDnpxfL2zOYJ1mFwrryWTz0advv1Ut4CJgf5uhDuDj5eUcAUoahrdY/56ebRWeraTjMt/00Sh3UDtjgHtQNHwcRGOC98BJEAEymycmYcWwOprTgcB6VZ5JK5TAJ+fXGLBm3FDAmn6oPPjR4rKCAoJCal2eAiQp2x0vxTPB3ALO2CRkwmDy5WohzBDwSEFKRwPbknEggCPB/imwrycgxX2NzoMCHhPkDwqYMr9tRcP5qNrMZHkVnOjRMWwLCcr8ohBVb1OMjxLwGCvjTikrsBOiA6fNyCrm8V1rP93iVPpwaE+gO0SsWmPiXB+jikdf6SizrT5qKasx5j8ABbHpFTx+vFXp9EnYQmLx02h1QTTrl6eDqxLnGjporxl3NL3agEvXdT0WmEost648sQOYAeJS9Q7bfUVoMGnjo4AZdUMQku50McDcMWcBPvr0SzbTAFDfvJqwLzgxwATnCgnp4wDl6Aa+Ax283gghmj+vj7feE2KBBRMW3FzOpLOADl0Isb5587h/U4gGvkt5v60Z1VLG8BhYjbzRwyQZemwAd6cCR5/XFWLYZRIMpX39AR0tjaGGiGzLVyhse5C9RKC6ai42ppWPKiBagOvaYk8lO7DajerabOZP46Lby5wKjw1HCRx7p9sVMOWGzb/vA1hwiWc6jm3MvQDTogQkiqIhJV0nBQBTU+3okKCFDy9WwferkHjtxib7t3xIUQtHxnIwtx4mpg26/HfwVNVDb4oI9RHmx5WGelRVlrtiw43zboCLaxv46AZeB3IlTkwouebTr1y2NjSpHz68WNFjHvupy3q8TFn3Hos2IAk4Ju5dCo8B3wP7VPr/FGaKiG+T+v+TQqIrOqMTL1VdWV1DdmcbO8KXBz6esmYWYKPwDL5b5FA1a0hwapHiom0r/cKaoqr+27/XcrS5UwSMbQAAAABJRU5ErkJggg==" alt="Project Documentation">
    </a>
</p>

The **Value Object Pattern** is a Python 🐍 package for building immutable, self-validating value objects 📦. It helps
move validation, normalization, primitive conversion, and domain-specific constraints out of scattered application code
and into small typed objects that can be reused across models, services, APIs, and tests.
<br><br>

## Table of Contents

- [📥 Installation](#installation)
- [📚 Documentation](#documentation)
- [⚡ Quick Start](#quick-start)
- [🧩 Core Ideas](#core-ideas)
- [🤔 Why Value Objects?](#why-value-objects)
- [📦 Core Models](#core-models)
- [✅ Reusable Value Objects](#reusable-value-objects)
- [🔁 Primitive Conversion](#primitive-conversion)
- [🤝 Contributing](#contributing)
- [🔑 License](#license)

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p><br><br>

<a name="installation"></a>

## 📥 Installation

You can install **Value Object Pattern** using `pip`:

```bash
pip install value-object-pattern
```

You can install the companion AI-agent skill from [skills.sh](https://www.skills.sh/) with Vercel's `skills` CLI:

```bash
npx skills add adriamontoto/value-object-pattern
```

Review the skill source in [`skills/value-object-pattern`](skills/value-object-pattern) before installing it in
sensitive environments.

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p><br><br>

<a name="documentation"></a>

## 📚 Documentation

The root README is the entry point. Deeper guides live in this repository and are linked here:

- [`docs/README.md`](docs/README.md): Documentation hub.
- [`docs/usage/README.md`](docs/usage/README.md): Custom value objects, validators, processors, and model composition.
- [`docs/catalog/README.md`](docs/catalog/README.md): Feature map by reusable value-object category.
- Catalog details: [`primitives`](docs/catalog/primitives/README.md), [`dates`](docs/catalog/dates/README.md),
  [`identifiers`](docs/catalog/identifiers/README.md), [`internet`](docs/catalog/internet/README.md), and
  [`money`](docs/catalog/money/README.md).
- [`docs/conversion/README.md`](docs/conversion/README.md): Primitive conversion and nested model behavior.
- [`AI Skill`](skills/README.md): Installable skill package that teaches AI agents how to use Value Object Pattern.

This [project's DeepWiki documentation](https://deepwiki.com/adriamontoto/value-object-pattern) is also available for
generated repository navigation.

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p><br><br>

<a name="quick-start"></a>

## ⚡ Quick Start

Create a value object by subclassing `ValueObject[T]` and adding validation hooks:

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


age = Age(value=42)

print(age.value)
# >>> 42
print(repr(age))
# >>> Age(value=42)
```

Use reusable value objects when the package already provides the constraint:

```python
from value_object_pattern.usables import NotEmptyStringValueObject, PositiveIntegerValueObject

name = NotEmptyStringValueObject(value='Ada')
quantity = PositiveIntegerValueObject(value=3)
```

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p><br><br>

<a name="core-ideas"></a>

## 🧩 Core Ideas

Value objects in this package are designed around a few consistent rules:

- They wrap exactly one value and expose it through `.value`.
- They validate input during construction.
- They can normalize input with `@process` hooks.
- They reject attribute mutation after construction.
- They compare by concrete class and wrapped value.
- They can customize validation error context with `title` and `parameter`.

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


name = LowerTrimmedName(value='  ADA  ')

assert name.value == 'ada'
```

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p><br><br>

<a name="why-value-objects"></a>

## 🤔 Why Value Objects?

Value objects make domain rules explicit. A plain `str`, `int`, or `dict` can carry almost anything, so every function
that receives it has to remember what "valid" means. A value object gives that rule a name and enforces it at the point
where the value enters the model.

Without a value object, the same rule tends to be repeated across services, controllers, tests, and serializers:

```python
def register_user(email: str, age: int) -> None:
    if '@' not in email:
        raise ValueError('Invalid email.')

    if age <= 0:
        raise ValueError('Invalid age.')
```

With value objects, the signature communicates the expected shape and invalid values are rejected before the rest of the
code depends on them:

```python
from value_object_pattern.usables import PositiveIntegerValueObject
from value_object_pattern.usables.internet import EmailAddressValueObject


def register_user(email: EmailAddressValueObject, age: PositiveIntegerValueObject) -> None:
    assert '@' in email.value
    assert age.value > 0
```

This is useful when a value has a reusable meaning: email address, positive quantity, trimmed name, country code, URL,
UUID, money identifier, or any project-specific concept such as `TenantSlug`, `OrderLimit`, or `CustomerName`.

Raw literals and primitives are still the right choice when the value is simple or intentionally exact:

- Use raw primitives inside low-level calculations where no domain rule is being expressed.
- Use hardcoded values for exact examples, snapshots, JSON, SQL, URLs, error messages, and public documentation output.
- Use explicit boundary values for deliberate limits such as zero, one, minimum length, maximum length, empty strings,
  first date, last date, or a known invalid format.
- Use `.value` when crossing into libraries, APIs, or storage layers that expect primitives.

```python
from value_object_pattern.usables import PositiveIntegerValueObject

quantity = PositiveIntegerValueObject(value=10)

assert quantity.value == 10
assert quantity.value + 5 == 15
```

The practical rule is simple: use value objects for named domain constraints, and use primitives for exact literals,
low-level operations, and boundary examples.

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p><br><br>

<a name="core-models"></a>

## 📦 Core Models

| Model | Purpose |
| --- | --- |
| `ValueObject[T]` | Base class for immutable validated single-value wrappers. |
| `EnumerationValueObject[E]` | Stores enum members while accepting enum members or raw enum values. |
| `UnionValueObject[T]` | Accepts and converts values that match a union annotation; supports subclass and inline construction. |
| `BaseModel` | Adds representation, equality, copying, and primitive conversion for aggregate-like models. |
| `ListValueObject[T]` | Immutable typed list wrapper; supports subclass and inline construction. |
| `DictValueObject[K, V]` | Immutable typed dictionary wrapper; supports subclass and inline construction. |

See [`docs/usage/README.md`](docs/usage/README.md) for examples of each model.

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p><br><br>

<a name="reusable-value-objects"></a>

## ✅ Reusable Value Objects

The package includes reusable validators for common shapes:

| Category | Examples |
| --- | --- |
| Primitives | strings, bytes, booleans, integers, floats, `None` / not-`None` |
| String formats | non-empty, trimmed, alpha, alphanumeric, lower/upper case, snake case, kebab case, secret strings |
| Dates | `date`, `datetime`, date strings, datetime strings, timezone objects, timezone names |
| Identifiers | UUIDs and UUID strings, world codes, Spanish identifiers and vehicle plates |
| Internet | URLs, hosts, domains, ports, emails, IP addresses, networks, MAC addresses, slugs, keys |
| Money | IBANs and credit card values |

See [`docs/catalog/README.md`](docs/catalog/README.md) for import paths and category guidance.

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p><br><br>

<a name="primitive-conversion"></a>

## 🔁 Primitive Conversion

`BaseModel`, `ListValueObject`, `DictValueObject`, and `UnionValueObject` can convert between primitive data and richer
types.

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

More details are available in [`docs/conversion/README.md`](docs/conversion/README.md).

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p><br><br>

<a name="contributing"></a>

## 🤝 Contributing

We love community help! Before you open an issue or pull request, please read:

- [`🤝 How to Contribute`](https://github.com/adriamontoto/value-object-pattern/blob/master/.github/CONTRIBUTING.md)
- [`🧭 Code of Conduct`](https://github.com/adriamontoto/value-object-pattern/blob/master/.github/CODE_OF_CONDUCT.md)
- [`🔐 Security Policy`](https://github.com/adriamontoto/value-object-pattern/blob/master/.github/SECURITY.md)

_Thank you for helping make **📦 Value Object Pattern** package awesome! 🌟_

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p><br><br>

<a name="license"></a>

## 🔑 License

This project is licensed under the terms of the [`MIT license`](https://github.com/adriamontoto/value-object-pattern/blob/master/LICENSE.md).

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p>
