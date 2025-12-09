"""
StringUuidV4ValueObject value object.
"""

from typing import NoReturn
from uuid import UUID

from value_object_pattern.decorators import validation

from .string_uuid_value_object import StringUuidValueObject


class StringUuidV4ValueObject(StringUuidValueObject):
    """
    StringUuidV4ValueObject value object ensures the provided value is a valid UUID version 4.

    Example:
    ```python
    from value_object_pattern.usables.identifiers import StringUuidV4ValueObject

    uuid = StringUuidV4ValueObject(value='3e9e0f3a-64a3-474f-9127-368e723f389f')
    print(repr(uuid))
    # >>> StringUuidV4ValueObject(value=3e9e0f3a-64a3-474f-9127-368e723f389f)
    ```
    """

    @validation(order=1)
    def _ensure_value_is_uuid4(self, value: str) -> None:
        """
        Ensures the value object `value` is a UUID version 4.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 4.
        """
        uuid_object = UUID(value)
        if uuid_object.version != 4:
            self._raise_value_is_not_uuid4(value=value)

    def _raise_value_is_not_uuid4(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a UUID version 4.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 4.
        """
        raise ValueError(f'StringUuidV4ValueObject value <<<{value}>>> must be a UUID version 4. Got version <<<{UUID(value).version}>>>.')  # noqa: E501  # fmt: skip
