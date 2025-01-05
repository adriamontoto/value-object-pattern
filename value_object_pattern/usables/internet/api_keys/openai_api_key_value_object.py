"""
OpenaiApiKeyValueObject value object.
"""

from re import fullmatch

from value_object_pattern.decorators import validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class OpenaiApiKeyValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    OpenaiApiKeyValueObject value object.
    """

    __OPENAI_API_KEY_VALUE_OBJECT_REGEX: str = r'^sk-[A-Za-z0-9]{20}T3BlbkFJ[A-Za-z0-9]{20}$'

    @validation(order=0)
    def _ensure_value_is_valid_openai_api_key(self, value: str) -> None:
        """
        Ensures the value object value is a valid OpenAI API Key.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not a valid OpenAI API Key.
        """
        if not fullmatch(pattern=self.__OPENAI_API_KEY_VALUE_OBJECT_REGEX, string=value):
            raise ValueError(f'OpenaiApiKeyValueObject value <<<{value}>>> is not a valid OpenAI API Key.')
