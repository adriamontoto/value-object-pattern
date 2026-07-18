"""
DomainOrLocalhostValueObject value object.
"""

from .domain_value_object import DomainValueObject


class DomainOrLocalhostValueObject(DomainValueObject):
    """
    DomainOrLocalhostValueObject ensures the provided value is a valid domain or localhost.

    Example:
    ```python
    from value_object_pattern.usables.internet import DomainOrLocalhostValueObject

    domain = DomainOrLocalhostValueObject(value='localhost')
    print(repr(domain))
    # >>> DomainOrLocalhostValueObject(value=localhost)
    ```
    """

    _DOMAIN_VALID_SINGLE_LABELS: frozenset[str] = frozenset({'localhost'})
