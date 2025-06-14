"""
UuidValueObject value object.
"""

from typing import Any, NoReturn
from uuid import UUID

from value_object_pattern.decorators import validation
from value_object_pattern.models import ValueObject


class UuidValueObject(ValueObject[UUID]):
    """
    UuidValueObject value object ensures the provided value is a valid UUID.

    Example:
    ```python
    from uuid import uuid4

    from value_object_pattern.usables.identifiers import UuidValueObject

    uuid = UuidValueObject(value=uuid4())

    print(repr(uuid))
    # >>> UuidValueObject(value=9908bb2d-54b4-426f-bef0-b09aa978ed21)
    ```
    """

    @validation(order=0)
    def _ensure_value_is_uuid(self, value: UUID) -> None:
        """
        Ensures the value object `value` is a UUID.

        Args:
            value (UUID): The provided value.

        Raises:
            TypeError: If the `value` is not a UUID.
        """
        if type(value) is not UUID:
            self._raise_value_is_not_uuid(value=value)

    def _raise_value_is_not_uuid(self, value: Any) -> NoReturn:
        """
        Raises a TypeError if the value object `value` is not a UUID.

        Args:
            value (Any): The provided value.

        Raises:
            TypeError: If the `value` is not a UUID.
        """
        raise TypeError(f'UuidValueObject value <<<{value}>>> must be a UUID. Got <<<{type(value).__name__}>>> type.')
