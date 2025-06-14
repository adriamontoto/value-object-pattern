"""
IntegerValueObject value object.
"""

from typing import Any, NoReturn

from value_object_pattern.decorators import validation
from value_object_pattern.models import ValueObject


class IntegerValueObject(ValueObject[int]):
    """
    IntegerValueObject value object ensures the provided value is an integer.

    Example:
    ```python
    from value_object_pattern.usables import IntegerValueObject

    integer = IntegerValueObject(value=1)

    print(repr(integer))
    # >>> IntegerValueObject(value=1)
    ```
    """

    @validation(order=0)
    def _ensure_value_is_integer(self, value: int) -> None:
        """
        Ensures the value object `value` is an integer.

        Args:
            value (int): The provided value.

        Raises:
            TypeError: If the `value` is not an integer.
        """
        if type(value) is not int:
            self._raise_value_is_not_integer(value=value)

    def _raise_value_is_not_integer(self, value: Any) -> NoReturn:
        """
        Raises a TypeError if the value object `value` is not an integer.

        Args:
            value (Any): The provided value.

        Raises:
            TypeError: If the `value` is not an integer.
        """
        raise TypeError(f'IntegerValueObject value <<<{value}>>> must be an integer. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip
