"""
DomainValueObject value object.
"""

from functools import lru_cache
from re import Pattern, compile as re_compile
from urllib.request import urlopen

from value_object_pattern import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


@lru_cache(maxsize=1)
def get_top_level_domains() -> set[str]:
    """
    Get top level domains from IANA.

    Args:
        url (str): The URL to get the top level domains.

    Returns:
        set[str]: The top level domains in lower case.

    References:
        https://data.iana.org/TLD/tlds-alpha-by-domain.txt
    """
    url = 'https://data.iana.org/TLD/tlds-alpha-by-domain.txt'
    with urlopen(url=url) as response:  # noqa: S310
        content = response.read().decode('utf-8')

    return {line.strip().lower() for line in content.splitlines() if line and not line.startswith('#')}


class DomainValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    DomainValueObject value object ensures the provided value is a valid domain.

    References:
        https://data.iana.org/TLD/tlds-alpha-by-domain.txt

    Example:
    ```python
    from value_object_pattern.usables.internet import DomainValueObject

    key = DomainValueObject(value='github.com')

    print(repr(key))
    # >>> DomainValueObject(value=github.com)
    ```
    """

    __DOMAIN_VALUE_OBJECT_MIN_LABEL_LENGTH: int = 1
    __DOMAIN_VALUE_OBJECT_MAX_LABEL_LENGTH: int = 63
    __DOMAIN_VALUE_OBJECT_MAX_DOMAIN_LENGTH: int = 253
    __DOMAIN_VALUE_OBJECT_REGEX: Pattern[str] = re_compile(pattern=r'^[a-zA-Z0-9-]+$')

    @process(order=0)
    def _ensure_domain_is_in_lowercase(self, value: str) -> str:
        """
        Ensure domain is in lowercase.

        Args:
            value (str): The domain value.

        Returns:
            str: The domain value in lowercase.
        """
        return value.lower()

    @process(order=1)
    def _ensure_domain_has_not_trailing_dot(self, value: str) -> str:
        """
        Ensure domain has not trailing dot.

        Args:
            value (str): The domain value.

        Returns:
            str: The domain value without trailing dot.
        """
        return value.rstrip('.')

    @validation(order=0)
    def _validate_top_level_domain(self, value: str) -> None:
        """
        Validate top level domain.

        Args:
            value (str): The domain value.

        Raises:
            ValueError: If domain value has not a valid top level domain.
        """
        if '.' not in value:
            raise ValueError(f'DomainValueObject value <<<{value}>>> has not a valid top level domain.')

        tdl = value.lower().rstrip('.').split(sep='.')[-1]
        if tdl not in get_top_level_domains():
            raise ValueError(f'DomainValueObject value <<<{value}>>> has not a valid top level domain <<<{tdl}>>>.')

    @validation(order=1)
    def _validate_domain_length(self, value: str) -> None:
        """
        Validate domain length.

        Args:
            value (str): The domain value.

        Raises:
            ValueError: If value length is longer than the maximum domain length.
        """
        if len(value) > self.__DOMAIN_VALUE_OBJECT_MAX_DOMAIN_LENGTH:
            raise ValueError(f'DomainValueObject value <<<{value}>>> length is longer than <<<{self.__DOMAIN_VALUE_OBJECT_MAX_DOMAIN_LENGTH}>>> characters.')  # noqa: E501  # fmt: skip

    @validation(order=2)
    def _validate_domain_labels(self, value: str) -> None:
        """
        Validate each label (label) according to standard DNS rules.
         - Label must be between 1 and 63 characters long.
         - Label must only contain letters, digits, or hyphens.
         - Label must not start or end with a hyphen.

        Args:
            value (str): The domain value.

        Raises:
            ValueError: If value has a label shorter than the minimum length.
            ValueError: If value has a label longer than the maximum length.
            ValueError: If value has a label starting with a hyphen.
            ValueError: If value has a label ending with a hyphen.
            ValueError: If value has a label containing invalid characters.
        """
        labels = value.lower().rstrip('.').split(sep='.')
        labels = labels[:-1] if len(labels) > 1 else labels  # remove top level domain
        for label in labels:
            if len(label) < self.__DOMAIN_VALUE_OBJECT_MIN_LABEL_LENGTH:
                raise ValueError(f'DomainValueObject value <<<{value}>>> has a label <<<{label}>>> shorter than <<<{self.__DOMAIN_VALUE_OBJECT_MIN_LABEL_LENGTH}>>> characters.')  # noqa: E501  # fmt: skip

            if len(label) > self.__DOMAIN_VALUE_OBJECT_MAX_LABEL_LENGTH:
                raise ValueError(f'DomainValueObject value <<<{value}>>> has a label <<<{label}>>> longer than <<<{self.__DOMAIN_VALUE_OBJECT_MAX_LABEL_LENGTH}>>> characters.')  # noqa: E501  # fmt: skip

            if label[0] == '-':
                raise ValueError(f'DomainValueObject value <<<{value}>>> has a label <<<{label}>>> that starts with a hyphen.')  # noqa: E501  # fmt: skip

            if label[-1] == '-':
                raise ValueError(f'DomainValueObject value <<<{value}>>> has a label <<<{label}>>> that ends with a hyphen.')  # noqa: E501  # fmt: skip

            if not self.__DOMAIN_VALUE_OBJECT_REGEX.fullmatch(string=label.encode(encoding='idna').decode(encoding='utf-8')):  # noqa: E501  # fmt: skip
                raise ValueError(f'DomainValueObject value <<<{value}>>> has a label <<<{label}>>> containing invalid characters. Only letters, digits, and hyphens are allowed.')  # noqa: E501  # fmt: skip
