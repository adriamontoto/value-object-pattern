"""
UuidV3ValueObject value object.
"""

from typing import Any, NoReturn
from uuid import UUID

from value_object_pattern.decorators import validation

from .uuid_value_object import UuidValueObject


class UuidV3ValueObject(UuidValueObject):
    """
    UuidV3ValueObject value object ensures the provided value is a valid UUID version 3.

    Example:
    ```python
    from uuid import NAMESPACE_DNS, uuid3

    from value_object_pattern.usables.identifiers import UuidV3ValueObject

    uuid = UuidV3ValueObject(value=uuid3(namespace=NAMESPACE_DNS, name='example.com'))
    print(repr(uuid))
    # >>> UuidV3ValueObject(value=9073926b-929f-31c2-abc9-fad77ae3e8eb)
    ```
    """

    @validation(order=1)
    def _ensure_value_is_uuid3(self, value: UUID) -> None:
        """
        Ensures the value object `value` is a UUID version 3.

        Args:
            value (UUID): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 3.
        """
        if value.version != 3:
            self._raise_value_is_not_uuid3(value=value)

    def _raise_value_is_not_uuid3(self, value: Any) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a UUID version 3.

        Args:
            value (Any): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 3.
        """
        raise ValueError(f'UuidV3ValueObject value <<<{value}>>> must be a UUID version 3. Got version <<<{value.version}>>>.')  # noqa: E501  # fmt: skip
