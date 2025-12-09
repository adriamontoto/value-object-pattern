"""
StringUuidV1ValueObject value object.
"""

from typing import NoReturn
from uuid import UUID

from value_object_pattern.decorators import validation

from .string_uuid_value_object import StringUuidValueObject


class StringUuidV1ValueObject(StringUuidValueObject):
    """
    StringUuidV1ValueObject value object ensures the provided value is a valid UUID version 1.

    Example:
    ```python
    from value_object_pattern.usables.identifiers import StringUuidV1ValueObject

    uuid = StringUuidV1ValueObject(value='53734b8c-d517-11f0-a57a-452bbcae0235')
    print(repr(uuid))
    # >>> StringUuidV1ValueObject(value=53734b8c-d517-11f0-a57a-452bbcae0235)
    ```
    """

    @validation(order=1)
    def _ensure_value_is_uuid1(self, value: str) -> None:
        """
        Ensures the value object `value` is a UUID version 1.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 1.
        """
        uuid_object = UUID(value)
        if uuid_object.version != 1:
            self._raise_value_is_not_uuid1(value=value)

    def _raise_value_is_not_uuid1(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a UUID version 1.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 1.
        """
        raise ValueError(f'StringUuidV1ValueObject value <<<{value}>>> must be a UUID version 1. Got version <<<{UUID(value).version}>>>.')  # noqa: E501  # fmt: skip
