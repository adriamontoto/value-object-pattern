"""
UuidV1ValueObject value object.
"""

from typing import Any, NoReturn
from uuid import UUID

from value_object_pattern.decorators import validation

from .uuid_value_object import UuidValueObject


class UuidV1ValueObject(UuidValueObject):
    """
    UuidV1ValueObject value object ensures the provided value is a valid UUID version 1.

    Example:
    ```python
    from uuid import uuid1

    from value_object_pattern.usables.identifiers import UuidV1ValueObject

    uuid = UuidV1ValueObject(value=uuid1())
    print(repr(uuid))
    # >>> UuidV1ValueObject(value=26afb422-824d-11f0-9bbf-325096b39f47)
    ```
    """

    @validation(order=1)
    def _ensure_value_is_uuid1(self, value: UUID) -> None:
        """
        Ensures the value object `value` is a UUID version 1.

        Args:
            value (UUID): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 1.
        """
        if value.version != 1:
            self._raise_value_is_not_uuid1(value=value)

    def _raise_value_is_not_uuid1(self, value: Any) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a UUID version 1.

        Args:
            value (Any): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 1.
        """
        raise ValueError(f'UuidV1ValueObject value <<<{value}>>> must be a UUID version 1. Got version <<<{value.version}>>>.')  # noqa: E501  # fmt: skip
