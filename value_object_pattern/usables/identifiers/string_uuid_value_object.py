"""
StringUuidValueObject value object.
"""

from __future__ import annotations

from uuid import UUID

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class StringUuidValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    StringUuidValueObject value object.

    Example:
    ```python
    from value_object_pattern.usables.identifiers import StringUuidValueObject

    uuid = StringUuidValueObject(value='9908bb2d-54b4-426f-bef0-b09aa978ed21')

    print(repr(uuid))
    # >>> StringUuidValueObject(value=9908bb2d-54b4-426f-bef0-b09aa978ed21)
    ```
    """

    @process(order=0)
    def _ensure_value_is_lower(self, value: str) -> str:
        """
        Ensures the value object value is lower UUID string.

        Args:
            value (str): Value.

        Returns:
            str: Value with the lower UUID string.
        """
        return value.lower()

    @validation(order=0)
    def _ensure_value_is_uuid(self, value: str) -> None:
        """
        Ensures the value object value is a UUID.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not a UUID.
        """
        try:
            UUID(hex=value)

        except ValueError as error:
            raise ValueError(f'StringUuidValueObject value <<<{value}>>> is not a valid UUID.') from error
