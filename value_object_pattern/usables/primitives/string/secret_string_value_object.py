"""
SecretStringValueObject value object.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from .string_value_object import StringValueObject


class SecretStringValueObject(StringValueObject):
    """
    SecretStringValueObject stores a string that is redacted in display-oriented output.

    Example:
    ```python
    from value_object_pattern.usables import SecretStringValueObject

    secret = SecretStringValueObject(value='hidden-value')

    print(secret)
    # >>> ********
    ```
    """

    _MASK: str = '********'

    @override
    def _value_for_display(self) -> str:
        """
        Returns the display-safe representation of the secret value.

        Returns:
            str: The redacted secret value.
        """
        return self._MASK
