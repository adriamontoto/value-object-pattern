"""
AlphanumericStringValueObject value object.
"""

from typing import NoReturn

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
            self._raise_value_is_not_alphanumeric(value=value)

    def _raise_value_is_not_alphanumeric(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not alphanumeric.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not alphanumeric.
        """
        raise ValueError(f'AlphanumericStringValueObject value <<<{value}>>> contains invalid characters. Only alphanumeric characters are allowed.')  # noqa: E501  # fmt: skip
