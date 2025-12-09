"""
UuidV4ValueObject value object.
"""

from typing import Any, NoReturn
from uuid import UUID

from value_object_pattern.decorators import validation

from .uuid_value_object import UuidValueObject


class UuidV4ValueObject(UuidValueObject):
    """
    UuidV4ValueObject value object ensures the provided value is a valid UUID version 4.

    Example:
    ```python
    from uuid import uuid4

    from value_object_pattern.usables.identifiers import UuidV4ValueObject

    uuid = UuidV4ValueObject(value=uuid4())
    print(repr(uuid))
    # >>> UuidV4ValueObject(value=3e9e0f3a-64a3-474f-9127-368e723f389f)
    ```
    """

    @validation(order=1)
    def _ensure_value_is_uuid4(self, value: UUID) -> None:
        """
        Ensures the value object `value` is a UUID version 4.

        Args:
            value (UUID): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 4.
        """
        if value.version != 4:
            self._raise_value_is_not_uuid4(value=value)

    def _raise_value_is_not_uuid4(self, value: Any) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a UUID version 4.

        Args:
            value (Any): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 4.
        """
        raise ValueError(f'UuidV4ValueObject value <<<{value}>>> must be a UUID version 4. Got version <<<{value.version}>>>.')  # noqa: E501  # fmt: skip
