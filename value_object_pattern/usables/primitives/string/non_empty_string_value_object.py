"""
NotEmptyStringValueObject value object.
"""

from typing import NoReturn

from value_object_pattern.decorators import validation

from .string_value_object import StringValueObject


class NotEmptyStringValueObject(StringValueObject):
    """
    NotEmptyStringValueObject value object ensures the provided value is not an empty string.

    Example:
    ```python
    from value_object_pattern.usables import NotEmptyStringValueObject

    string = NotEmptyStringValueObject(value='abcd1234')

    print(repr(string))
    # >>> NotEmptyStringValueObject(value='abcd1234')
    ```
    """

    @validation(order=0)
    def _ensure_value_is_not_empty_string(self, value: str) -> None:
        """
        Ensures the value object `value` is not an empty string.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is an empty string.
        """
        if not value:
            self._raise_value_is_empty_string(value=value)

    def _raise_value_is_empty_string(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is an empty string.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is an empty string.
        """
        raise ValueError(f'NotEmptyStringValueObject value <<<{value}>>> is an empty string. Only non-empty strings are allowed.')  # noqa: E501  # fmt: skip
