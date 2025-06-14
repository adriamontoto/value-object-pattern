"""
AlphaStringValueObject value object.
"""

from typing import NoReturn

from value_object_pattern.decorators import validation

from .string_value_object import StringValueObject


class AlphaStringValueObject(StringValueObject):
    """
    AlphaStringValueObject value object ensures the provided value is alpha.

    Example:
    ```python
    from value_object_pattern.usables import AlphaStringValueObject

    string = AlphaStringValueObject(value='abcd')

    print(repr(string))
    # >>> AlphaStringValueObject(value='abcd')
    ```
    """

    @validation(order=0)
    def _ensure_value_is_alpha(self, value: str) -> None:
        """
        Ensures the value object `value` is alpha.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not alpha.
        """
        if not value.isalpha():
            self._raise_value_is_not_alpha(value=value)

    def _raise_value_is_not_alpha(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not alpha.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not alpha.
        """
        raise ValueError(f'AlphaStringValueObject value <<<{value}>>> contains invalid characters. Only alpha characters are allowed.')  # noqa: E501  # fmt: skip
