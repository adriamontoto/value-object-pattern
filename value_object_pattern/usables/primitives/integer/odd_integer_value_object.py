"""
OddIntegerValueObject value object.
"""

from value_object_pattern.decorators import validation

from .integer_value_object import IntegerValueObject


class OddIntegerValueObject(IntegerValueObject):
    """
    OddIntegerValueObject value object.
    """

    @validation(order=0)
    def ensure_value_is_odd_number(self, value: int) -> None:
        """
        Ensures the value object value is an odd number.

        Args:
            value (int): Value.

        Raises:
            ValueError: If the value is not an odd number.
        """
        if value % 2 == 0:
            raise ValueError(f'OddIntegerValueObject value <<<{value}>>> must be an odd number.')
