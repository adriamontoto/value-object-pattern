"""
EvenIntegerValueObject value object.
"""

from value_object_pattern.decorators import validation

from .integer_value_object import IntegerValueObject


class EvenIntegerValueObject(IntegerValueObject):
    """
    EvenIntegerValueObject value object.
    """

    @validation(order=0)
    def ensure_value_is_even_number(self, value: int) -> None:
        """
        Ensures the value object value is an even number.

        Args:
            value (int): Value.

        Raises:
            ValueError: If the value is not an even number.
        """
        if value % 2 != 0:
            raise ValueError(f'EvenIntegerValueObject value <<<{value}>>> must be an even number.')
