"""
NegativeIntegerValueObject value object.
"""

from value_object_pattern.decorators import validation

from .integer_value_object import IntegerValueObject


class NegativeIntegerValueObject(IntegerValueObject):
    """
    NegativeIntegerValueObject value object.

    Example:
    ```python
    from value_object_pattern.usables import IntegerValueObject

    integer = IntegerValueObject(value=-1)

    print(repr(integer))
    # >>> IntegerValueObject(value=-1)
    ```
    """

    @validation(order=0)
    def _ensure_value_is_negative_integer(self, value: int) -> None:
        """
        Ensures the value object value is a negative integer.

        Args:
            value (int): Value.

        Raises:
            ValueError: If the value is not a negative integer.
        """
        if value >= 0:
            raise ValueError(f'NegativeIntegerValueObject value <<<{value}>>> must be a negative integer.')
