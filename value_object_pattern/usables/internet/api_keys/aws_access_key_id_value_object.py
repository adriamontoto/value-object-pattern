"""
AwsAccessKeyValueObject value object.
"""

from re import fullmatch

from value_object_pattern.decorators import validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class AwsAccessKeyValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    AwsAccessKeyValueObject value object.
    """

    __AWS_ACCESS_KEY_VALUE_OBJECT_REGEX: str = r'^(AKIA|ASIA)[A-Z0-9]{16}$'

    @validation(order=0)
    def _ensure_value_is_valid_aws_access_key(self, value: str) -> None:
        """
        Ensures the value object value is a valid AWS Access Key ID.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not a valid AWS Access Key ID.
        """
        if not fullmatch(pattern=self.__AWS_ACCESS_KEY_VALUE_OBJECT_REGEX, string=value):
            raise ValueError(f'AwsAccessKeyValueObject value <<<{value}>>> is not a valid AWS Access Key ID.')
