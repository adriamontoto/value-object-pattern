# Date And Time Value Objects

Date and time value objects validate Python date/time objects and common string representations. They are useful at API
and persistence boundaries where plain strings should be normalized into explicit domain types.

## Imports

```python
from value_object_pattern.usables.dates import (
    DateValueObject,
    DatetimeValueObject,
    StringDateValueObject,
    StringDatetimeValueObject,
    StringTimezoneValueObject,
    TimezoneValueObject,
)
```

## Catalog

| Value Object | Rule |
| --- | --- |
| `DateValueObject` | Accepts exact `datetime.date` values and exposes date comparison helpers. |
| `DatetimeValueObject` | Accepts exact `datetime.datetime` values and exposes datetime comparison helpers. |
| `StringDateValueObject` | Accepts string dates in the configured package format. |
| `StringDatetimeValueObject` | Accepts string datetimes in the configured package format. |
| `TimezoneValueObject` | Accepts timezone objects. |
| `StringTimezoneValueObject` | Accepts timezone names as strings. |

## Example

```python
from datetime import date

from value_object_pattern.usables.dates import DateValueObject

birthday = DateValueObject(value=date(year=1990, month=5, day=1))

assert birthday.is_later_than(reference_date=date(year=1980, month=1, day=1))
```

## Guidance

- Use object-backed date/time value objects inside domain models.
- Use string-backed date/time value objects at text-oriented boundaries.
- Pass explicit reference dates in tests instead of relying on the current date.
- Keep timezone validation separate from business scheduling rules such as working days or service windows.
