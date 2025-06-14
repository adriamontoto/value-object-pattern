"""
LowercaseStringValueObject value object.
"""

from typing import NoReturn

from value_object_pattern.decorators import validation

from .string_value_object import StringValueObject


class LowercaseStringValueObject(StringValueObject):
    """
    LowercaseStringValueObject value object ensures the provided value is lowercase.

    Example:
    ```python
    from value_object_pattern.usables import LowercaseStringValueObject

    string = LowercaseStringValueObject(value='abcd1234')

    print(repr(string))
    # >>> LowercaseStringValueObject(value='abcd1234')
    ```
    """

    @validation(order=0)
    def _ensure_value_is_lowercase(self, value: str) -> None:
        """
        Ensures the value object `value` is lowercase.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not lowercase.
        """
        if not value.islower():
            self._raise_value_is_not_lowercase(value=value)

    def _raise_value_is_not_lowercase(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not lowercase.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not lowercase.
        """
        raise ValueError(f'LowercaseStringValueObject value <<<{value}>>> contains uppercase characters. Only lowercase characters are allowed.')  # noqa: E501  # fmt: skip
