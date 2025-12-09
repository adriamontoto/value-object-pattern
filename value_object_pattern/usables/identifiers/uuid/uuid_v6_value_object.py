"""
UuidV6ValueObject value object.
"""

from typing import Any, NoReturn
from uuid import UUID

from value_object_pattern.decorators import validation

from .uuid_value_object import UuidValueObject


class UuidV6ValueObject(UuidValueObject):
    """
    UuidV6ValueObject value object ensures the provided value is a valid UUID version 6.

    Example:
    ```python
    from uuid import uuid6

    from value_object_pattern.usables.identifiers import UuidV6ValueObject

    uuid = UuidV6ValueObject(value=uuid6())
    print(repr(uuid))
    # >>> UuidV6ValueObject(value=1f0d455c-76e5-6210-b032-46ef6b2a93e1)
    ```
    """

    @validation(order=1)
    def _ensure_value_is_uuid6(self, value: UUID) -> None:
        """
        Ensures the value object `value` is a UUID version 6.

        Args:
            value (UUID): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 6.
        """
        if value.version != 6:
            self._raise_value_is_not_uuid6(value=value)

    def _raise_value_is_not_uuid6(self, value: Any) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a UUID version 6.

        Args:
            value (Any): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 6.
        """
        raise ValueError(f'UuidV6ValueObject value <<<{value}>>> must be a UUID version 6. Got version <<<{value.version}>>>.')  # noqa: E501  # fmt: skip
