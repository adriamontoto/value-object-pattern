"""
PositiveFloatValueObject value object.
"""

from value_object_pattern.decorators import validation

from .float_value_object import FloatValueObject


class PositiveFloatValueObject(FloatValueObject):
    """
    PositiveFloatValueObject value object ensures the provided value is a positive float.

    Example:
    ```python
    from value_object_pattern.usables import FloatValueObject

    float_ = FloatValueObject(value=0.5)

    print(repr(float_))
    # >>> FloatValueObject(value=0.5)
    ```
    """

    @validation(order=0)
    def _ensure_value_is_positive_float(self, value: float) -> None:
        """
        Ensures the value object `value` is a positive float.

        Args:
            value (float): The provided value.

        Raises:
            ValueError: If the `value` is not a positive float.
        """
        if value <= 0:
            raise ValueError(f'PositiveFloatValueObject value <<<{value}>>> must be a positive float.')
