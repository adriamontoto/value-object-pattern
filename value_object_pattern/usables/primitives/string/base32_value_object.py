"""
Base32StringValueObject value object.
"""

from re import Pattern, compile as re_compile

from value_object_pattern.decorators import process, validation

from .string_value_object import StringValueObject


class Base32StringValueObject(StringValueObject):
    """
    Base32StringValueObject value object.

    Example:
    ```python
    from value_object_pattern.usables import Base32StringValueObject

    string = Base32StringValueObject(value='RGIZTI==')

    print(repr(string))
    # >>> Base32StringValueObject(value='RGIZTI==')
    ```
    """

    __HEXADECIMAL_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'^[a-zA-Z2-7]+=*$')

    @process(order=0)
    def _ensure_value_is_uppercase(self, value: str) -> str:
        """
        Ensures the value object value is uppercase.

        Args:
            value (str): Value.

        Returns:
            str: Uppercase value.
        """
        return value.upper()

    @validation(order=0)
    def _ensure_value_is_base32(self, value: str) -> None:
        """
        Ensures the value object value is Base32.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not Base32.
        """
        if not self.__HEXADECIMAL_VALUE_OBJECT_REGEX.fullmatch(string=value):
            raise ValueError(f'Base32StringValueObject value <<<{value}>>> contains invalid characters. Only base32 characters are allowed.')  # noqa: E501  # fmt: skip
