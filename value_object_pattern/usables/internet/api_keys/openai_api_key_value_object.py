"""
OpenaiApiKeyValueObject value object.
"""

from re import Pattern, compile as re_compile

from value_object_pattern.decorators import validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class OpenaiApiKeyValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    OpenaiApiKeyValueObject value object ensures the provided value is a valid OpenAI API Key.

    Example:
    ```python
    from value_object_pattern.usables.internet import OpenaiApiKeyValueObject

    key = OpenaiApiKeyValueObject(value='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')  # gitleaks:allow

    print(repr(key))
    # >>> OpenaiApiKeyValueObject(value=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)  # gitleaks:allow
    ```
    """

    __OPENAI_API_KEY_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'^sk-[a-zA-Z0-9]{20}T3BlbkFJ[a-zA-Z0-9]{20}$')  # noqa: E501  # fmt: skip

    @validation(order=0)
    def _ensure_value_is_valid_openai_api_key(self, value: str) -> None:
        """
        Ensures the value object value is a valid OpenAI API Key.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not a valid OpenAI API Key.
        """
        if not self.__OPENAI_API_KEY_VALUE_OBJECT_REGEX.fullmatch(string=value):
            raise ValueError(f'OpenaiApiKeyValueObject value <<<{value}>>> is not a valid OpenAI API Key.')
