# Date And Time Value Objects

Date and time value objects validate Python date/time objects and common string representations. They are useful at API
and persistence boundaries where plain strings should be normalized into explicit domain types.

## Imports

```python
from value_object_pattern.usables.dates import (
    DateValueObject,
    DatetimeValueObject,
    DurationValueObject,
    NegativeDurationValueObject,
    NegativeOrZeroDurationValueObject,
    PositiveDurationValueObject,
    PositiveOrZeroDurationValueObject,
    StringDateValueObject,
    StringDatetimeValueObject,
    StringTimeValueObject,
    StringTimezoneValueObject,
    TimeValueObject,
    TimezoneValueObject,
)
```

## Catalog

| Value Object                        | Rule                                                                                                      |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `DateValueObject`                   | Accepts exact `datetime.date` values and exposes date comparison helpers.                                 |
| `DatetimeValueObject`               | Accepts exact `datetime.datetime` values and exposes datetime comparison helpers.                         |
| `DurationValueObject`               | Accepts signed `datetime.timedelta` values; factories and helpers support seconds, minutes, hours, and days. |
| `NegativeDurationValueObject`       | Accepts durations lower than zero.                                                                        |
| `NegativeOrZeroDurationValueObject` | Accepts durations lower than or equal to zero.                                                            |
| `PositiveDurationValueObject`       | Accepts durations greater than zero.                                                                      |
| `PositiveOrZeroDurationValueObject` | Accepts durations greater than or equal to zero.                                                          |
| `StringDateValueObject`             | Accepts string dates in the configured package format.                                                    |
| `StringDatetimeValueObject`         | Accepts string datetimes in the configured package format.                                                |
| `TimeValueObject`                   | Accepts exact `datetime.time` values, including naive and timezone-aware times.                            |
| `StringTimeValueObject`             | Accepts strings parsed by `datetime.time.fromisoformat` and stores normalized ISO time strings.            |
| `TimezoneValueObject`               | Accepts timezone objects.                                                                                 |
| `StringTimezoneValueObject`         | Accepts timezone names as strings.                                                                        |

## Example

```python
from datetime import date, time

from value_object_pattern.usables.dates import (
    DateValueObject,
    PositiveDurationValueObject,
    StringTimeValueObject,
    TimeValueObject,
)

birthday = DateValueObject(value=date(year=1990, month=5, day=1))

assert birthday.is_later_than(reference_date=date(year=1980, month=1, day=1))

timeout = PositiveDurationValueObject.from_minutes(minutes=5)
assert timeout.to_seconds() == 300.0

meeting_time = TimeValueObject(value=time(hour=14, minute=30))
text_time = StringTimeValueObject(value="14:30")

assert meeting_time.value == time(hour=14, minute=30)
assert text_time.value == "14:30:00"
```

## Guidance

- Use object-backed date/time value objects inside domain models.
- Use string-backed date/time value objects at text-oriented boundaries.
- Use a sign-constrained duration for domain values such as positive timeouts; use `DurationValueObject` when signed
  differences are valid and `TimeValueObject` for a time of day.
- Pass explicit reference dates in tests instead of relying on the current date.
- Keep timezone validation separate from business scheduling rules such as working days or service windows.
