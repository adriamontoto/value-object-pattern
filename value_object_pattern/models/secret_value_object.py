"""
Composition marker for display-redacted value objects.
"""


class SecretValueObject:
    """
    Redact the display output of any accompanying value-object base.

    This composition-only marker does not store or validate values. Combine it with any `ValueObject` subclass in either
    inheritance order. The accompanying value object supplies the wrapped type, validation, processing, and primitive
    conversion behavior.

    The raw value remains available through `.value` and primitive conversion. Redaction is a presentation guard, not
    encryption or secure secret storage.

    Example:
    ```python
    from value_object_pattern import SecretValueObject
    from value_object_pattern.usables import StringValueObject


    class SecretString(SecretValueObject, StringValueObject):
        pass


    secret = SecretString(value='hidden-value')
    print(secret)
    # >>> ********
    ```
    """

    __slots__ = ()

    _MASK: str = '********'

    def _secret_value_for_display(self) -> str:
        """
        Return the fixed display mask.

        Returns:
            str: Redacted display value.
        """
        return self._MASK
