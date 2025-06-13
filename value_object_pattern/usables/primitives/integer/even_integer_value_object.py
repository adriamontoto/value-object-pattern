"""
EvenIntegerValueObject value object.
"""

from value_object_pattern.decorators import validation

from .integer_value_object import IntegerValueObject


class EvenIntegerValueObject(IntegerValueObject):
    """
    EvenIntegerValueObject value object ensures the provided value is an even integer.

    Example:
    ```python
    from value_object_pattern.usables import EvenIntegerValueObject

    integer = EvenIntegerValueObject(value=2)

    print(repr(integer))
    # >>> EvenIntegerValueObject(value=2)
    ```
    """

    @validation(order=0)
    def _ensure_value_is_even_number(self, value: int) -> None:
        """
        Ensures the value object `value` is an even number.

        Args:
            value (int): The provided value.

        Raises:
            ValueError: If the `value` is not an even number.
        """
        if value % 2 != 0:
            raise ValueError(f'EvenIntegerValueObject value <<<{value}>>> must be an even number.')
