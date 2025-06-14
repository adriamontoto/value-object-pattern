"""
TrimmedStringValueObject value object.
"""

from typing import NoReturn

from value_object_pattern.decorators import validation

from .string_value_object import StringValueObject


class TrimmedStringValueObject(StringValueObject):
    """
    TrimmedStringValueObject value object ensures the provided value is trimmed.

    Example:
    ```python
    from value_object_pattern.usables import TrimmedStringValueObject

    string = TrimmedStringValueObject(value='abcd1234')

    print(repr(string))
    # >>> TrimmedStringValueObject(value='abcd1234')
    ```
    """

    @validation(order=0)
    def _ensure_value_is_trimmed(self, value: str) -> None:
        """
        Ensures the value object `value` is trimmed.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not trimmed.
        """
        if value != value.strip():
            self._raise_value_is_not_trimmed(value=value)

    def _raise_value_is_not_trimmed(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not trimmed.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not trimmed.
        """
        raise ValueError(f'TrimmedStringValueObject value <<<{value}>>> contains leading or trailing whitespaces. Only trimmed values are allowed.')  # noqa: E501  # fmt: skip
