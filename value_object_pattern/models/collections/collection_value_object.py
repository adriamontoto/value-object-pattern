"""
CollectionValueObject module.
"""

from collections.abc import Collection
from typing import Any, NoReturn

from value_object_pattern.decorators import validation
from value_object_pattern.models.value_object import ValueObject


class CollectionValueObject(ValueObject[Collection[Any]]):
    """
    CollectionValueObject is a value object that ensures the provided value is from a collection.

    Example:
    ```python
    from value_object_pattern.models.collections import CollectionValueObject

    collection = CollectionValueObject(value=[1, 2, 3])
    print(collection)
    # >>> [1, 2, 3]
    ```
    """

    def __contains__(self, item: Any) -> bool:
        """
        Returns True if the value object value contains the item, otherwise False.

        Args:
            item (Any): The item to check.

        Returns:
            bool: True if the value object value contains the item, otherwise False.

        Example:
        ```python
        from value_object_pattern.models.collections import CollectionValueObject

        collection = CollectionValueObject(value=[1, 2, 3])
        print(1 in collection)
        # >>> True
        ```
        """
        return item in self._value

    def __len__(self) -> int:
        """
        Returns the length of the value object value.

        Returns:
            int: The length of the value object value.

        Example:
        ```python
        from value_object_pattern.models.collections import CollectionValueObject

        collection = CollectionValueObject(value=[1, 2, 3])
        print(len(collection))
        # >>> 3
        ```
        """
        return len(self._value)

    @validation(order=0)
    def _ensure_value_is_from_collection(self, value: Collection[Any]) -> None:
        """
        Ensures the value object `value` is a collection.

        Args:
            value (Collection[Any]): The provided value.

        Raises:
            TypeError: If the `value` is not a collection.
        """
        if not isinstance(value, Collection):
            self._raise_value_is_not_collection(value=value)

    def _raise_value_is_not_collection(self, value: Any) -> NoReturn:
        """
        Raises a TypeError if the value object `value` is not a collection.

        Args:
            value (Any): The provided value.

        Raises:
            TypeError: If the `value` is not a collection.
        """
        raise TypeError(f'CollectionValueObject value <<<{value}>>> must be a collection. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip

    def is_empty(self) -> bool:
        """
        Returns True if the value object value is empty, otherwise False.

        Returns:
            bool: True if the value object value is empty, otherwise False.

        Example:
        ```python
        from value_object_pattern.models.collections import CollectionValueObject

        collection = CollectionValueObject(value=[])
        print(collection.is_empty())
        # >>> True
        ```
        """
        return not self._value
