"""
FloatValueObject value object.
"""

from value_object_pattern.decorators import validation
from value_object_pattern.models import ValueObject


class FloatValueObject(ValueObject[float]):
    """
    FloatValueObject value object ensures the provided value is a float.

    Example:
    ```python
    from value_object_pattern.usables import FloatValueObject

    float_ = FloatValueObject(value=0.5)

    print(repr(float_))
    # >>> FloatValueObject(value=0.5)
    ```
    """

    @validation(order=0)
    def _ensure_value_is_float(self, value: float) -> None:
        """
        Ensures the value object `value` is a float.

        Args:
            value (float): The provided value.

        Raises:
            TypeError: If the `value` is not a float.
        """
        if type(value) is not float:
            raise TypeError(f'FloatValueObject value <<<{value}>>> must be a float. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip
