"""
NoneValueObject value object.
"""

from typing import Any, NoReturn

from value_object_pattern.decorators import validation
from value_object_pattern.models import ValueObject


class NoneValueObject(ValueObject[None]):
    """
    NoneValueObject value object ensures the provided value is None.

    Example:
    ```python
    from value_object_pattern.usables import NoneValueObject

    none = NoneValueObject(value=None)

    print(repr(none))
    # >>> NoneValueObject(value=None)
    ```
    """

    @validation(order=0)
    def _ensure_value_is_none(self, value: None) -> None:
        """
        Ensures the value object `value` is None.

        Args:
            value (None): The provided value.

        Raises:
            TypeError: If the `value` is not None.
        """
        if value is not None:
            self._raise_value_is_not_none(value=value)

    def _raise_value_is_not_none(self, value: Any) -> NoReturn:
        """
        Raises a TypeError if the value object `value` is not None.

        Args:
            value (Any): The provided value.

        Raises:
            TypeError: If the `value` is not None.
        """
        raise TypeError(f'NoneValueObject value <<<{value}>>> must be None. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip
