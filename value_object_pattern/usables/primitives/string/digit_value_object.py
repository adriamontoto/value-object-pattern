"""
DigitStringValueObject value object.
"""

from typing import NoReturn

from value_object_pattern.decorators import validation

from .string_value_object import StringValueObject


class DigitStringValueObject(StringValueObject):
    """
    DigitStringValueObject value object ensures the provided value is digit.

    Example:
    ```python
    from value_object_pattern.usables import DigitStringValueObject

    string = DigitStringValueObject(value='1234')

    print(repr(string))
    # >>> DigitStringValueObject(value='1234')
    ```
    """

    @validation(order=0)
    def _ensure_value_is_digit(self, value: str) -> None:
        """
        Ensures the value object `value` is digit.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not digit.
        """
        if not value.isdigit():
            self._raise_value_is_not_digit(value=value)

    def _raise_value_is_not_digit(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not digit.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not digit.
        """
        raise ValueError(f'DigitStringValueObject value <<<{value}>>> contains invalid characters. Only digit characters are allowed.')  # noqa: E501  # fmt: skip
