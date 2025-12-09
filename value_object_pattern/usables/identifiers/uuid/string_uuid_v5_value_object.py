"""
StringUuidV5ValueObject value object.
"""

from typing import NoReturn
from uuid import UUID

from value_object_pattern.decorators import validation

from .string_uuid_value_object import StringUuidValueObject


class StringUuidV5ValueObject(StringUuidValueObject):
    """
    StringUuidV5ValueObject value object ensures the provided value is a valid UUID version 5.

    Example:
    ```python
    from value_object_pattern.usables.identifiers import StringUuidV5ValueObject

    uuid = StringUuidV5ValueObject(value='cfbff0d1-9375-5685-968c-48ce8b15ae17')
    print(repr(uuid))
    # >>> StringUuidV5ValueObject(value=cfbff0d1-9375-5685-968c-48ce8b15ae17)
    ```
    """

    @validation(order=1)
    def _ensure_value_is_uuid5(self, value: str) -> None:
        """
        Ensures the value object `value` is a UUID version 5.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 5.
        """
        uuid_object = UUID(value)
        if uuid_object.version != 5:
            self._raise_value_is_not_uuid5(value=value)

    def _raise_value_is_not_uuid5(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a UUID version 5.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 5.
        """
        raise ValueError(f'StringUuidV5ValueObject value <<<{value}>>> must be a UUID version 5. Got version <<<{UUID(value).version}>>>.')  # noqa: E501  # fmt: skip
