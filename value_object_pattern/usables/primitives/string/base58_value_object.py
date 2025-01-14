"""
Base58StringValueObject value object.
"""

from re import Pattern, compile as re_compile

from value_object_pattern.decorators import validation

from .string_value_object import StringValueObject


class Base58StringValueObject(StringValueObject):
    """
    Base58StringValueObject value object.

    Example:
    ```python
    from value_object_pattern.usables import Base58StringValueObject

    string = Base58StringValueObject(value='3mJr7AoU')

    print(repr(string))
    # >>> Base58StringValueObject(value='3mJr7AoU')
    ```
    """

    __BASE58_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'^[a-km-zA-HJ-NP-Z1-9]+$')

    @validation(order=0)
    def _ensure_value_is_base58(self, value: str) -> None:
        """
        Ensures the value object value is Base58 encoded.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not a valid Base58 string.
        """
        if not self.__BASE58_VALUE_OBJECT_REGEX.fullmatch(string=value):
            raise ValueError(f'Base58StringValueObject value <<<{value}>>> contains invalid characters. Only base58 characters are allowed.')  # noqa: E501  # fmt: skip
