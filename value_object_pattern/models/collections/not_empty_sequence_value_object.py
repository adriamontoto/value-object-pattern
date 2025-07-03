"""
NotEmptySequenceValueObject module.
"""

from collections.abc import Sequence
from typing import Any, NoReturn

from value_object_pattern.decorators import validation

from .sequence_value_object import SequenceValueObject


class NotEmptySequenceValueObject(SequenceValueObject):
    """
    NotEmptySequenceValueObject is a value object that ensures the provided value is from a sequence.

    Example:
    ```python
    from value_object_pattern.models.collections import NotEmptySequenceValueObject

    sequence = NotEmptySequenceValueObject(value=[1, 2, 3])
    print(sequence)
    # >>> [1, 2, 3]
    ```
    """

    @validation(order=0)
    def _ensure_value_is_not_empty_sequence(self, value: Sequence[Any]) -> None:
        """
        Ensures the value object `value` is not an empty sequence.

        Args:
            value (Sequence[Any]): The provided value.

        Raises:
            TypeError: If the `value` is an empty sequence.
        """
        if not value:
            self._raise_value_is_empty_sequence(value=value)

    def _raise_value_is_empty_sequence(self, value: Any) -> NoReturn:
        """
        Raises a TypeError if the value object `value` is an empty sequence.

        Args:
            value (Any): The provided value.

        Raises:
            TypeError: If the `value` is an empty sequence.
        """
        raise TypeError(f'NotEmptySequenceValueObject value <<<{value}>>> must not be an empty sequence.')
