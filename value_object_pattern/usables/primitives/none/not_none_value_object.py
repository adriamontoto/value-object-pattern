"""
NotNoneValueObject value object.
"""

from typing import Any, NoReturn

from value_object_pattern.decorators import validation
from value_object_pattern.models import ValueObject


class NotNoneValueObject(ValueObject[Any]):
    """
    NotNoneValueObject value object ensures the provided value is not None.

    Example:
    ```python
    from value_object_pattern.usables import NotNoneValueObject

    none = NotNoneValueObject(value='test')

    print(repr(none))
    # >>> NotNoneValueObject(value=test)
    ```
    """

    @validation(order=0)
    def _ensure_value_is_not_none(self, value: Any) -> None:
        """
        Ensures the value object `value` is not None.

        Args:
            value (Any): The provided value.

        Raises:
            TypeError: If the `value` is None.
        """
        if value is None:
            self._raise_value_is_not_none(value=value)

    def _raise_value_is_not_none(self, value: Any) -> NoReturn:
        """
        Raises a TypeError if the value object `value` is None.

        Args:
            value (Any): The provided value.

        Raises:
            TypeError: If the `value` is None.
        """
        raise TypeError(f'NotNoneValueObject value <<<{value}>>> must be not None.')
