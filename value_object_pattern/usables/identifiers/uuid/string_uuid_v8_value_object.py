"""
StringUuidV8ValueObject value object.
"""

from typing import NoReturn
from uuid import UUID

from value_object_pattern.decorators import validation

from .string_uuid_value_object import StringUuidValueObject


class StringUuidV8ValueObject(StringUuidValueObject):
    """
    StringUuidV8ValueObject value object ensures the provided value is a valid UUID version 8.

    Example:
    ```python
    from value_object_pattern.usables.identifiers import StringUuidV8ValueObject

    uuid = StringUuidV8ValueObject(value='1f6b82d1-1a39-4607-8a28-4dd1453104d3')

    print(repr(uuid))
    # >>> StringUuidV8ValueObject(value=1f6b82d1-1a39-4607-8a28-4dd1453104d3)
    ```
    """

    @validation(order=1)
    def _ensure_value_is_uuid8(self, value: str) -> None:
        """
        Ensures the value object `value` is a UUID version 8.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 8.
        """
        uuid_object = UUID(value)
        if uuid_object.version != 8:
            self._raise_value_is_not_uuid8(value=value)

    def _raise_value_is_not_uuid8(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a UUID version 8.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 8.
        """
        raise ValueError(f'StringUuidV8ValueObject value <<<{value}>>> must be a UUID version 8. Got version <<<{UUID(value).version}>>>.')  # noqa: E501  # fmt: skip
