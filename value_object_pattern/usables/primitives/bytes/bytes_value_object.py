"""
BytesValueObject value object.
"""

from typing import Any, NoReturn

from value_object_pattern.decorators import validation
from value_object_pattern.models import ValueObject


class BytesValueObject(ValueObject[bytes]):
    """
    BytesValueObject value object ensures the provided value is bytes.

    Example:
    ```python
    from value_object_pattern.usables import BytesValueObject

    bytes_ = BytesValueObject(value=b'aad30be7ce99fb0fe411')

    print(repr(bytes_))
    # >>> BytesValueObject(value=b'aad30be7ce99fb0fe411')
    ```
    """

    @validation(order=0)
    def _ensure_value_is_bytes(self, value: bytes) -> None:
        """
        Ensures the value object `value` is bytes.

        Args:
            value (bytes): The provided value.

        Raises:
            TypeError: If the `value` is not bytes.
        """
        if type(value) is not bytes:
            self._raise_value_is_not_bytes(value=value)

    def _raise_value_is_not_bytes(self, value: Any) -> NoReturn:
        """
        Raises a TypeError if the value object `value` is not bytes.

        Args:
            value (Any): The provided value.

        Raises:
            TypeError: If the `value` is not bytes.
        """
        raise TypeError(f'BytesValueObject value <<<{str(object=value)}>>> must be bytes. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip
