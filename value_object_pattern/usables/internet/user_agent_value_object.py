"""
UserAgentValueObject value object.
"""

from value_object_pattern.usables import NotEmptyStringValueObject, PrintableStringValueObject, TrimmedStringValueObject


class UserAgentValueObject(NotEmptyStringValueObject, PrintableStringValueObject, TrimmedStringValueObject):
    """
    UserAgentValueObject ensures the provided value is a non-empty, trimmed, printable user agent string.

    Example:
    ```python
    from value_object_pattern.usables.internet import UserAgentValueObject

    user_agent = UserAgentValueObject(value='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15')

    print(repr(user_agent))
    # >>> UserAgentValueObject(value='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15')
    ```
    """
