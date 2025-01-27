"""
PositiveIntegerValueObject value object.
"""

from value_object_pattern.decorators import validation

from .integer_value_object import IntegerValueObject


class PositiveIntegerValueObject(IntegerValueObject):
    """
    PositiveIntegerValueObject value object.

    Example:
    ```python
    from value_object_pattern.usables import PositiveIntegerValueObject

    integer = PositiveIntegerValueObject(value=1)

    print(repr(integer))
    # >>> PositiveIntegerValueObject(value=1)
    ```
    """

    @validation(order=0)
    def _ensure_value_is_positive_integer(self, value: int) -> None:
        """
        Ensures the value object value is a positive integer.

        Args:
            value (int): Value.

        Raises:
            ValueError: If the value is not a positive integer.
        """
        if value <= 0:
            raise ValueError(f'PositiveIntegerValueObject value <<<{value}>>> must be a positive integer.')
