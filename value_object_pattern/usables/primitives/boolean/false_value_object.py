"""
FalseValueObject value object.
"""

from typing import NoReturn

from value_object_pattern.decorators import validation

from .boolean_value_object import BooleanValueObject


class FalseValueObject(BooleanValueObject):
    """
    FalseValueObject value object ensures the provided value is false.

    Example:
    ```python
    from value_object_pattern.usables import BooleanValueObject

    boolean = BooleanValueObject(value=False)

    print(repr(boolean))
    # >>> BooleanValueObject(value=False)
    ```
    """

    @validation(order=0)
    def _ensure_value_is_false(self, value: bool) -> None:
        """
        Ensures the value object `value` is false.

        Args:
            value (bool): The provided value.

        Raises:
            ValueError: If the `value` is not false.
        """
        if value:
            self._raise_value_is_not_false(value=value)

    def _raise_value_is_not_false(self, value: bool) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not false.

        Args:
            value (bool): The provided value.

        Raises:
            ValueError: If the `value` is not false.
        """
        raise ValueError(f'FalseValueObject value <<<{value}>>> must be false.')
