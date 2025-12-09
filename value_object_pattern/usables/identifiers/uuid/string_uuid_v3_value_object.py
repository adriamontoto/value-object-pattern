"""
StringUuidV3ValueObject value object.
"""

from typing import NoReturn
from uuid import UUID

from value_object_pattern.decorators import validation

from .string_uuid_value_object import StringUuidValueObject


class StringUuidV3ValueObject(StringUuidValueObject):
    """
    StringUuidV3ValueObject value object ensures the provided value is a valid UUID version 3.

    Example:
    ```python
    from value_object_pattern.usables.identifiers import StringUuidV3ValueObject

    uuid = StringUuidV3ValueObject(value='9073926b-929f-31c2-abc9-fad77ae3e8eb')
    print(repr(uuid))
    # >>> StringUuidV3ValueObject(value=9073926b-929f-31c2-abc9-fad77ae3e8eb)
    ```
    """

    @validation(order=1)
    def _ensure_value_is_uuid3(self, value: str) -> None:
        """
        Ensures the value object `value` is a UUID version 3.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 3.
        """
        uuid_object = UUID(value)
        if uuid_object.version != 3:
            self._raise_value_is_not_uuid3(value=value)

    def _raise_value_is_not_uuid3(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a UUID version 3.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 3.
        """
        raise ValueError(f'StringUuidV3ValueObject value <<<{value}>>> must be a UUID version 3. Got version <<<{UUID(value).version}>>>.')  # noqa: E501  # fmt: skip
