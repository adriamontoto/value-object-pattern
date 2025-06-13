"""
TrueValueObject value object.
"""

from value_object_pattern.decorators import validation

from .boolean_value_object import BooleanValueObject


class TrueValueObject(BooleanValueObject):
    """
    TrueValueObject value object ensures the provided value is true.

    Example:
    ```python
    from value_object_pattern.usables import BooleanValueObject

    boolean = BooleanValueObject(value=True)

    print(repr(boolean))
    # >>> BooleanValueObject(value=True)
    ```
    """

    @validation(order=0)
    def _ensure_value_is_true(self, value: bool) -> None:
        """
        Ensures the value object `value` is true.

        Args:
            value (bool): The provided value.

        Raises:
            ValueError: If the `value` is not true.
        """
        if not value:
            raise ValueError(f'TrueValueObject value <<<{value}>>> must be true.')
