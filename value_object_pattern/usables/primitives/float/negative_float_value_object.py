"""
NegativeFloatValueObject value object.
"""

from value_object_pattern.decorators import validation

from .float_value_object import FloatValueObject


class NegativeFloatValueObject(FloatValueObject):
    """
    NegativeFloatValueObject value object ensures the provided value is a negative float.

    Example:
    ```python
    from value_object_pattern.usables import FloatValueObject

    float_ = FloatValueObject(value=-0.5)

    print(repr(float_))
    # >>> FloatValueObject(value=-0.5)
    ```
    """

    @validation(order=0)
    def _ensure_value_is_negative_float(self, value: float) -> None:
        """
        Ensures the value object `value` is a negative float.

        Args:
            value (float): The provided value.

        Raises:
            ValueError: If the `value` is not a negative float.
        """
        if value >= 0:
            raise ValueError(f'NegativeFloatValueObject value <<<{value}>>> must be a negative float.')
