"""
GitHubPersonalAccessTokenValueObject value object.
"""

from re import fullmatch

from value_object_pattern.decorators import validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class GitHubPersonalAccessTokenValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    GitHubPersonalAccessTokenValueObject value object.
    """

    __GITHUB_PERSONAL_ACCESS_TOKEN_VALUE_OBJECT_REGEX: str = r'^ghp_[0-9A-Za-z]{36}$'

    @validation(order=0)
    def _ensure_value_is_valid_github_pat(self, value: str) -> None:
        """
        Ensures the value object value is a valid GitHub Personal Access Token.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not a valid GitHub Personal Access Token
        """
        if not fullmatch(pattern=self.__GITHUB_PERSONAL_ACCESS_TOKEN_VALUE_OBJECT_REGEX, string=value):
            raise ValueError(f'GitHubPersonalAccessTokenValueObject value <<<{value}>>> is not a valid GitHub Personal Access Token.')  # noqa: E501  # fmt: skip
