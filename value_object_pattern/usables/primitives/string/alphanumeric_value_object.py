"""
AlphanumericStringValueObject value object.
"""

from value_object_pattern.decorators import validation

from .string_value_object import StringValueObject


class AlphanumericStringValueObject(StringValueObject):
    """
    AlphanumericStringValueObject value object ensures the provided value is alphanumeric.

    Example:
    ```python
    from value_object_pattern.usables import AlphanumericStringValueObject

    string = AlphanumericStringValueObject(value='abcd1234')

    print(repr(string))
    # >>> AlphanumericStringValueObject(value='abcd1234')
    ```
    """

    @validation(order=0)
    def _ensure_value_is_alphanumeric(self, value: str) -> None:
        """
        Ensures the value object `value` is alphanumeric.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not alphanumeric.
        """
        if not value.isalnum():
            raise ValueError(f'AlphanumericStringValueObject value <<<{value}>>> contains invalid characters. Only alphanumeric characters are allowed.')  # noqa: E501  # fmt: skip
