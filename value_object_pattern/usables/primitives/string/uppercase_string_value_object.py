"""
UppercaseStringValueObject value object.
"""

from value_object_pattern.decorators import validation

from .string_value_object import StringValueObject


class UppercaseStringValueObject(StringValueObject):
    """
    UppercaseStringValueObject value object.

    Example:
    ```python
    from value_object_pattern.usables import UppercaseStringValueObject

    string = UppercaseStringValueObject(value='ABCD1234')

    print(repr(string))
    # >>> UppercaseStringValueObject(value='ABCD1234')
    ```
    """

    @validation(order=0)
    def _ensure_value_is_uppercase(self, value: str) -> None:
        """
        Ensures the value object value is uppercase.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not uppercase.
        """
        if not value.isupper():
            raise ValueError(f'UppercaseStringValueObject value <<<{value}>>> contains lowercase characters. Only uppercase characters are allowed.')  # noqa: E501  # fmt: skip
