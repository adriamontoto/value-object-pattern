"""
BooleanValueObject value object.
"""

from typing import Any, NoReturn

from value_object_pattern.decorators import validation
from value_object_pattern.models import ValueObject


class BooleanValueObject(ValueObject[bool]):
    """
    BooleanValueObject value object ensures the provided value is a boolean.

    Example:
    ```python
    from value_object_pattern.usables import BooleanValueObject

    boolean = BooleanValueObject(value=True)

    print(repr(boolean))
    # >>> BooleanValueObject(value=True)
    ```
    """

    @validation(order=0)
    def _ensure_value_is_boolean(self, value: bool) -> None:
        """
        Ensures the value object `value` is a boolean.

        Args:
            value (bool): The provided value.

        Raises:
            TypeError: If the `value` is not a boolean.
        """
        if type(value) is not bool:
            self._raise_value_is_not_boolean(value=value)

    def _raise_value_is_not_boolean(self, value: Any) -> NoReturn:
        """
        Raises a TypeError if the value object `value` is not a boolean.

        Args:
            value (Any): The provided value.

        Raises:
            TypeError: If the `value` is not a boolean.
        """
        raise TypeError(f'BooleanValueObject value <<<{value}>>> must be a boolean. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip
