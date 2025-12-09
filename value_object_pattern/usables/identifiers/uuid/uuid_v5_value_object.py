"""
UuidV5ValueObject value object.
"""

from typing import Any, NoReturn
from uuid import UUID

from value_object_pattern.decorators import validation

from .uuid_value_object import UuidValueObject


class UuidV5ValueObject(UuidValueObject):
    """
    UuidV5ValueObject value object ensures the provided value is a valid UUID version 5.

    Example:
    ```python
    from uuid import NAMESPACE_DNS, uuid5

    from value_object_pattern.usables.identifiers import UuidV5ValueObject

    uuid = UuidV5ValueObject(value=uuid5(namespace=NAMESPACE_DNS, name='example.com'))
    print(repr(uuid))
    # >>> UuidV5ValueObject(value=cfbff0d1-9375-5685-968c-48ce8b15ae17)
    ```
    """

    @validation(order=1)
    def _ensure_value_is_uuid5(self, value: UUID) -> None:
        """
        Ensures the value object `value` is a UUID version 5.

        Args:
            value (UUID): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 5.
        """
        if value.version != 5:
            self._raise_value_is_not_uuid5(value=value)

    def _raise_value_is_not_uuid5(self, value: Any) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a UUID version 5.

        Args:
            value (Any): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 5.
        """
        raise ValueError(f'UuidV5ValueObject value <<<{value}>>> must be a UUID version 5. Got version <<<{value.version}>>>.')  # noqa: E501  # fmt: skip
