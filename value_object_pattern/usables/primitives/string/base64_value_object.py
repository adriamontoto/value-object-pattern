"""
Base64StringValueObject value object.
"""

from re import Pattern, compile as re_compile

from value_object_pattern.decorators import validation

from .string_value_object import StringValueObject


class Base64StringValueObject(StringValueObject):
    """
    Base64StringValueObject value object.

    Example:
    ```python
    from value_object_pattern.usables import Base64StringValueObject

    string = Base64StringValueObject(value='29ybGQ==')

    print(repr(string))
    # >>> Base64StringValueObject(value='29ybGQ==')
    ```
    """

    __BASE64_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'^[a-zA-Z0-9+/]+=*$')

    @validation(order=0)
    def _ensure_value_is_base64(self, value: str) -> None:
        """
        Ensures the value object value is Base64 encoded.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not a valid Base64 string.
        """
        if not self.__BASE64_VALUE_OBJECT_REGEX.fullmatch(string=value):
            raise ValueError(f'Base64StringValueObject value <<<{value}>>> contains invalid characters. Only base64 characters are allowed.')  # noqa: E501  # fmt: skip
