"""
Base56StringValueObject value object.
"""

from re import Pattern, compile as re_compile

from value_object_pattern.decorators import validation

from .string_value_object import StringValueObject


class Base56StringValueObject(StringValueObject):
    """
    Base56StringValueObject value object.

    Example:
    ```python
    from value_object_pattern.usables import Base56StringValueObject

    string = Base56StringValueObject(value='5EKAKz6H')

    print(repr(string))
    # >>> Base56StringValueObject(value='5EKAKz6H')
    ```
    """

    __BASE56_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'^[a-hj-km-np-zA-HJ-KM-NP-Z1-9]+$')

    @validation(order=0)
    def _ensure_value_is_base56(self, value: str) -> None:
        """
        Ensures the value object value is Base56 encoded.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not a valid Base56 string.
        """
        if not self.__BASE56_VALUE_OBJECT_REGEX.fullmatch(string=value):
            raise ValueError(f'Base56StringValueObject value <<<{value}>>> contains invalid characters. Only base56 characters are allowed.')  # noqa: E501  # fmt: skip
