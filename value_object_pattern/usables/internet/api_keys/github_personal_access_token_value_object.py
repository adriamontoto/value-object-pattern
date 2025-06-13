"""
GitHubPersonalAccessTokenValueObject value object.
"""

from re import Pattern, compile as re_compile

from value_object_pattern.decorators import validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class GitHubPersonalAccessTokenValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    GitHubPersonalAccessTokenValueObject value object ensures the provided value is a valid GitHub Personal Access
    Token.

    Example:
    ```python
    from value_object_pattern.usables.internet import GitHubPersonalAccessTokenValueObject

    key = GitHubPersonalAccessTokenValueObject(value='ghp_cgq4ZrHmFu0lLPl7ajKAwgMPnT5zhF000000')  # gitleaks:allow

    print(repr(key))
    # >>> GitHubPersonalAccessTokenValueObject(value=ghp_cgq4ZrHmFu0lLPl7ajKAwgMPnT5zhF000000)  # gitleaks:allow
    ```
    """

    __GITHUB_PERSONAL_ACCESS_TOKEN_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'^ghp_[a-zA-Z0-9]{36}$')

    @validation(order=0)
    def _ensure_value_is_valid_github_pat(self, value: str) -> None:
        """
        Ensures the value object value is a valid GitHub Personal Access Token.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not a valid GitHub Personal Access Token
        """
        if not self.__GITHUB_PERSONAL_ACCESS_TOKEN_VALUE_OBJECT_REGEX.fullmatch(string=value):
            raise ValueError(f'GitHubPersonalAccessTokenValueObject value <<<{value}>>> is not a valid GitHub Personal Access Token.')  # noqa: E501  # fmt: skip
