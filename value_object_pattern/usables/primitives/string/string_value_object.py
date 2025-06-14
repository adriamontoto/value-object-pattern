"""
StringValueObject value object.
"""

from typing import Any, NoReturn

from value_object_pattern.decorators import validation
from value_object_pattern.models import ValueObject


class StringValueObject(ValueObject[str]):
    """
    StringValueObject value object ensures the provided value is a string.

    Example:
    ```python
    from value_object_pattern.usables import StringValueObject

    string = StringValueObject(value='abcd1234')

    print(repr(string))
    # >>> StringValueObject(value='abcd1234')
    ```
    """

    @validation(order=0)
    def _ensure_value_is_string(self, value: str) -> None:
        """
        Ensures the value object `value` is a string.

        Args:
            value (str): The provided value.

        Raises:
            TypeError: If the `value` is not a string.
        """
        if type(value) is not str:
            self._raise_value_is_not_string(value=value)

    def _raise_value_is_not_string(self, value: Any) -> NoReturn:
        """
        Raises a TypeError if the value object `value` is not a string.

        Args:
            value (Any): The provided value.

        Raises:
            TypeError: If the `value` is not a string.
        """
        raise TypeError(f'StringValueObject value <<<{value}>>> must be a string. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip
