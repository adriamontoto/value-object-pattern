"""
UuidV7ValueObject value object.
"""

from typing import Any, NoReturn
from uuid import UUID

from value_object_pattern.decorators import validation

from .uuid_value_object import UuidValueObject


class UuidV7ValueObject(UuidValueObject):
    """
    UuidV7ValueObject value object ensures the provided value is a valid UUID version 7.

    Example:
    ```python
    from uuid import uuid7

    from value_object_pattern.usables.identifiers import UuidV7ValueObject

    uuid = UuidV7ValueObject(value=uuid7())
    print(repr(uuid))
    # >>> UuidV7ValueObject(value=019afedd-025c-7f00-b22f-796d93c9b9cb)
    ```
    """

    @validation(order=1)
    def _ensure_value_is_uuid7(self, value: UUID) -> None:
        """
        Ensures the value object `value` is a UUID version 7.

        Args:
            value (UUID): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 7.
        """
        if value.version != 7:
            self._raise_value_is_not_uuid7(value=value)

    def _raise_value_is_not_uuid7(self, value: Any) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a UUID version 7.

        Args:
            value (Any): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 7.
        """
        raise ValueError(f'UuidV7ValueObject value <<<{value}>>> must be a UUID version 7. Got version <<<{value.version}>>>.')  # noqa: E501  # fmt: skip
