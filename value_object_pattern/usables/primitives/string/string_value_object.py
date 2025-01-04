"""
StringValueObject value object.
"""

from value_object_pattern.decorators import validation
from value_object_pattern.models import ValueObject


class StringValueObject(ValueObject[str]):
    """
    StringValueObject value object.
    """

    @validation(order=0)
    def ensure_value_is_string(self, value: str) -> None:
        """
        Ensures the value object value is a string.

        Args:
            value (str): Value.

        Raises:
            TypeError: If the value is not a string.
        """
        if type(value) is not str:
            raise TypeError(f'StringValueObject value <<<{value}>>> must be a string. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip
