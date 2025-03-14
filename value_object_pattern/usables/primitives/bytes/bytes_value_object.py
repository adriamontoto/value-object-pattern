"""
BytesValueObject value object.
"""

from value_object_pattern.decorators import validation
from value_object_pattern.models import ValueObject


class BytesValueObject(ValueObject[bytes]):
    """
    BytesValueObject value object.

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
        Ensures the value object value is bytes.

        Args:
            value (bytes): Value.

        Raises:
            TypeError: If the value is not bytes.
        """
        if type(value) is not bytes:
            raise TypeError(f'BytesValueObject value <<<{str(object=value)}>>> must be bytes. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip
