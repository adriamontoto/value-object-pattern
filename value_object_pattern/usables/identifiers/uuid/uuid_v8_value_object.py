"""
UuidV8ValueObject value object.
"""

from typing import Any, NoReturn
from uuid import UUID

from value_object_pattern.decorators import validation

from .uuid_value_object import UuidValueObject


class UuidV8ValueObject(UuidValueObject):
    """
    UuidV8ValueObject value object ensures the provided value is a valid UUID version 8.

    Example:
    ```python
    from uuid import uuid8

    from value_object_pattern.usables.identifiers import UuidV8ValueObject

    uuid = UuidV8ValueObject(value=uuid8())
    print(repr(uuid))
    # >>> UuidV8ValueObject(value=1f6b82d1-1a39-4607-8a28-4dd1453104d3)
    ```
    """

    @validation(order=1)
    def _ensure_value_is_uuid8(self, value: UUID) -> None:
        """
        Ensures the value object `value` is a UUID version 8.

        Args:
            value (UUID): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 8.
        """
        if value.version != 8:
            self._raise_value_is_not_uuid8(value=value)

    def _raise_value_is_not_uuid8(self, value: Any) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a UUID version 8.

        Args:
            value (Any): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 8.
        """
        raise ValueError(f'UuidV8ValueObject value <<<{value}>>> must be a UUID version 8. Got version <<<{value.version}>>>.')  # noqa: E501  # fmt: skip
