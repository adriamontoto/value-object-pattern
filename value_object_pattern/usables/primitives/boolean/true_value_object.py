"""
TrueValueObject value object.
"""

from value_object_pattern.decorators import validation

from .boolean_value_object import BooleanValueObject


class TrueValueObject(BooleanValueObject):
    """
    TrueValueObject value object.
    """

    @validation(order=0)
    def ensure_value_is_true(self, value: bool) -> None:
        """
        Ensures the value object value is true.

        Args:
            value (bool): Value.

        Raises:
            ValueError: If the value is not true.
        """
        if not value:
            raise ValueError(f'TrueValueObject value <<<{value}>>> must be true.')
