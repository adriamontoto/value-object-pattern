"""
StringUuidV7ValueObject value object.
"""

from typing import NoReturn
from uuid import UUID

from value_object_pattern.decorators import validation

from .string_uuid_value_object import StringUuidValueObject


class StringUuidV7ValueObject(StringUuidValueObject):
    """
    StringUuidV7ValueObject value object ensures the provided value is a valid UUID version 7.

    Example:
    ```python
    from value_object_pattern.usables.identifiers import StringUuidV7ValueObject

    uuid = StringUuidV7ValueObject(value='019afedd-025c-7f00-b22f-796d93c9b9cb')
    print(repr(uuid))
    # >>> StringUuidV7ValueObject(value=019afedd-025c-7f00-b22f-796d93c9b9cb)
    ```
    """

    @validation(order=1)
    def _ensure_value_is_uuid7(self, value: str) -> None:
        """
        Ensures the value object `value` is a UUID version 7.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 7.
        """
        uuid_object = UUID(value)
        if uuid_object.version != 7:
            self._raise_value_is_not_uuid7(value=value)

    def _raise_value_is_not_uuid7(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a UUID version 7.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a UUID version 7.
        """
        raise ValueError(f'StringUuidV7ValueObject value <<<{value}>>> must be a UUID version 7. Got version <<<{UUID(value).version}>>>.')  # noqa: E501  # fmt: skip
