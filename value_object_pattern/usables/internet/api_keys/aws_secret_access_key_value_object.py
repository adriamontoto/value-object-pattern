"""
AwsSecretAccessKeyValueObject value object.
"""

from re import fullmatch

from value_object_pattern.decorators import validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class AwsSecretAccessKeyValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    AwsSecretAccessKeyValueObject value object.
    """

    __AWS_SECRET_ACCESS_KEY_VALUE_OBJECT_REGEX: str = r'^[A-Za-z0-9/+=]{40}$'

    @validation(order=0)
    def _ensure_value_is_valid_aws_secret_access_key(self, value: str) -> None:
        """
        Ensures the value object value is a valid AWS Secret Access Key.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not a valid AWS Secret Access Key.
        """
        if not fullmatch(pattern=self.__AWS_SECRET_ACCESS_KEY_VALUE_OBJECT_REGEX, string=value):
            raise ValueError(f'AwsSecretAccessKeyValueObject value <<<{value}>>> is not a valid AWS Secret Access Key.')
