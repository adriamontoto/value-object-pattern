"""
AwsSecretAccessKeyValueObject value object.
"""

from re import Pattern, compile as re_compile

from value_object_pattern.decorators import validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class AwsSecretAccessKeyValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    AwsSecretAccessKeyValueObject value object ensures the provided value is a valid AWS Secret Access Key.

    Example:
    ```python
    from value_object_pattern.usables.internet import AwsSecretAccessKeyValueObject

    key = AwsSecretAccessKeyValueObject(value='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY')  # gitleaks:allow

    print(repr(key))
    # >>> AwsSecretAccessKeyValueObject(value=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY)  # gitleaks:allow
    ```
    """

    __AWS_SECRET_ACCESS_KEY_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'^[a-zA-Z0-9/+=]{40}$')

    @validation(order=0)
    def _ensure_value_is_valid_aws_secret_access_key(self, value: str) -> None:
        """
        Ensures the value object value is a valid AWS Secret Access Key.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not a valid AWS Secret Access Key.
        """
        if not self.__AWS_SECRET_ACCESS_KEY_VALUE_OBJECT_REGEX.fullmatch(string=value):
            raise ValueError(f'AwsSecretAccessKeyValueObject value <<<{value}>>> is not a valid AWS Secret Access Key.')
