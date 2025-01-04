"""
FalseValueObject value object.
"""

from value_object_pattern.decorators import validation

from .boolean_value_object import BooleanValueObject


class FalseValueObject(BooleanValueObject):
    """
    FalseValueObject value object.
    """

    @validation(order=0)
    def _ensure_value_is_false(self, value: bool) -> None:
        """
        Ensures the value object value is false.

        Args:
            value (bool): Value.

        Raises:
            ValueError: If the value is not false.
        """
        if value:
            raise ValueError(f'FalseValueObject value <<<{value}>>> must be false.')
