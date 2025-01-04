"""
IntegerValueObject value object.
"""

from value_object_pattern.decorators import validation
from value_object_pattern.models import ValueObject


class IntegerValueObject(ValueObject[int]):
    """
    IntegerValueObject value object.
    """

    @validation(order=0)
    def ensure_value_is_integer(self, value: int) -> None:
        """
        Ensures the value object value is an integer.

        Args:
            value (int): Value.

        Raises:
            TypeError: If the value is not an integer.
        """
        if type(value) is not int:
            raise TypeError(f'IntegerValueObject value <<<{value}>>> must be an integer. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip
