"""
ResendApiKeyValueObject value object.
"""

from re import Pattern, compile as re_compile

from value_object_pattern.decorators import validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class ResendApiKeyValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    ResendApiKeyValueObject value object ensures the provided value is a valid Resend API Key.

    Example:
    ```python
    from value_object_pattern.usables.internet import ResendApiKeyValueObject

    key = ResendApiKeyValueObject(value='re_c1tpEyD8_NKFusih9vKVQknRAQfmFcWCv')  # gitleaks:allow

    print(repr(key))
    # >>> ResendApiKeyValueObject(value=re_c1tpEyD8_NKFusih9vKVQknRAQfmFcWCv)  # gitleaks:allow
    ```
    """

    __RESEND_API_KEY_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'^re_[a-zA-Z0-9-_]{30,}$')

    @validation(order=0)
    def _ensure_value_is_valid_resend_api_key(self, value: str) -> None:
        """
        Ensures the value object value is a valid Resend API Key.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not a valid Resend API Key.
        """
        if not self.__RESEND_API_KEY_VALUE_OBJECT_REGEX.fullmatch(string=value):
            raise ValueError(f'ResendApiKeyValueObject value <<<{value}>>> is not a valid Resend API Key.')
