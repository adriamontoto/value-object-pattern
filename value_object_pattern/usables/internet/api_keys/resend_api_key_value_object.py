"""
ResendApiKeyValueObject value object.
"""

from re import fullmatch

from value_object_pattern.decorators import validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class ResendApiKeyValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    ResendApiKeyValueObject value object.
    """

    __RESEND_API_KEY_VALUE_OBJECT_REGEX: str = r'^re_[0-9A-Za-z-_]{30,}$'

    @validation(order=0)
    def _ensure_value_is_valid_resend_api_key(self, value: str) -> None:
        """
        Ensures the value object value is a valid Resend API Key.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not a valid Resend API Key.
        """
        if not fullmatch(pattern=self.__RESEND_API_KEY_VALUE_OBJECT_REGEX, string=value):
            raise ValueError(f'ResendApiKeyValueObject value <<<{value}>>> is not a valid Resend API Key.')
