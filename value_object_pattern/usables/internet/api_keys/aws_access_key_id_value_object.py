"""
AwsAccessKeyValueObject value object.
"""

from re import Pattern, compile as re_compile

from value_object_pattern.decorators import validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class AwsAccessKeyValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    AwsAccessKeyValueObject value object ensures the provided value is a valid AWS Access Key ID.

    Example:
    ```python
    from value_object_pattern.usables.internet import AwsAccessKeyValueObject

    key = AwsAccessKeyValueObject(value='AKIAIOSFODNN7EXAMPLE')  # gitleaks:allow

    print(repr(key))
    # >>> AwsAccessKeyValueObject(value=AKIAIOSFODNN7EXAMPLE)  # gitleaks:allow
    ```
    """

    __AWS_ACCESS_KEY_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'^(AKIA|ASIA)[A-Z0-9]{16}$')

    @validation(order=0)
    def _ensure_value_is_valid_aws_access_key(self, value: str) -> None:
        """
        Ensures the value object value is a valid AWS Access Key ID.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not a valid AWS Access Key ID.
        """
        if not self.__AWS_ACCESS_KEY_VALUE_OBJECT_REGEX.fullmatch(string=value):
            raise ValueError(f'AwsAccessKeyValueObject value <<<{value}>>> is not a valid AWS Access Key ID.')
