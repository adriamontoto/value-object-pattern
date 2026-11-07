"""
Calendar calculations shared by date and datetime value objects.
"""

from calendar import monthrange
from datetime import date, timedelta


def calculate_age(*, value: date, reference: date) -> int:
    """
    Calculate completed calendar years between an ordered pair of dates or datetimes. Clamp leap-day anniversaries to
    the last day of February. Keep the reference calendar month as the upper bound when datetime offsets place the
    reference in an earlier local month. Calendar arithmetic resets the datetime fold before comparing an anniversary,
    including at daylight-saving transitions.

    Args:
        value (date): The date or datetime to calculate the age from.
        reference (date): The date or datetime to calculate the age to.

    Returns:
        int: The number of completed calendar years between the two dates or datetimes.
    """
    months = (reference.year - value.year) * 12 + reference.month - value.month
    years = max(0, months // 12)
    if years == 0:
        return 0

    year = value.year + years
    anniversary = value.replace(year=year, day=min(value.day, monthrange(year, value.month)[1])) + timedelta(0)

    return years - int(anniversary > reference)
