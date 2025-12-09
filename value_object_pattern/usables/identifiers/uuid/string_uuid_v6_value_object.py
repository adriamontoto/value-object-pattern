"""
StringUuidV6ValueObject value object.
"""

from typing import NoReturn
from uuid import UUID

from value_object_pattern.decorators import validation

from .string_uuid_value_object import StringUuidValueObject


class StringUuidV6ValueObject(StringUuidValueObject):
    """
    StringUuidV6ValueObject value object ensures the provided value is a valid UUID version 6.

    Example:
    ```python
    from value_object_pattern.usables.identifiers import StringUuidV6ValueObject

    uuid = StringUuidV6ValueObject(value='1f0d455c-76e5-6210-b032-46ef6b2a93e1')

    print(repr(uuid))
    # >>> StringUuidV6ValueObject(value=1f0d455c-76e5-6210-b032-46ef6b2a93e1)
    ```
    """

    @validation(order=1)
    def _ensure_value_is_uuid6(self, value: str) -> None:
        """
        Ensures the value object `value` is a UUID version 6.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 6.
        """
        uuid_object = UUID(value)
        if uuid_object.version != 6:
            self._raise_value_is_not_uuid6(value=value)

    def _raise_value_is_not_uuid6(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a UUID version 6.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 6.
        """
        raise ValueError(f'StringUuidV6ValueObject value <<<{value}>>> must be a UUID version 6. Got version <<<{UUID(value).version}>>>.')  # noqa: E501  # fmt: skip
