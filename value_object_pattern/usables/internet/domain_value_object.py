"""
DomainValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .utils import get_tld_dict


class DomainValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    DomainValueObject value object ensures the provided value is a valid domain.

    References:
        TLD Domains: https://data.iana.org/TLD/tlds-alpha-by-domain.txt

    Example:
    ```python
    from value_object_pattern.usables.internet import DomainValueObject

    domain = DomainValueObject(value='github.com')
    print(repr(domain))
    # >>> DomainValueObject(value=github.com)
    ```
    """

    _DOMAIN_MIN_LABEL_LENGTH: int = 1
    _DOMAIN_MAX_LABEL_LENGTH: int = 63
    _DOMAIN_MAX_DOMAIN_LENGTH: int = 253
    _DOMAIN_REGEX: Pattern[str] = re_compile(pattern=r'[0-9a-zA-Z-]+')

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

    @validation(order=0, early_process=True)
    def _validate_top_level_domain(self, value: str, processed_value: str) -> None:
        """
        Validate top level domain.

        Args:
            value (str): The domain value.
            processed_value (str): The early processed value.

        Raises:
            ValueError: If domain value has not a valid top level domain.
        """
        if '.' not in processed_value:
            self._raise_value_has_not_valid_top_level_domain(value=value)

        tdl = processed_value.split(sep='.')[-1]
        if tdl not in get_tld_dict():
            self._raise_value_has_not_valid_top_level_domain(value=value)

    def _raise_value_has_not_valid_top_level_domain(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value has not a valid top level domain.

        Args:
            value (str): The invalid domain value.

        Raises:
            ValueError: If the value has not a valid top level domain.
        """
        raise ValueError(f'DomainValueObject value <<<{value}>>> has not a valid top level domain.')

    @validation(order=1, early_process=True)
    def _validate_domain_length(self, value: str, processed_value: str) -> None:
        """
        Validate domain length.

        Args:
            value (str): The domain value.
            processed_value (str): The early processed value.

        Raises:
            ValueError: If value length is longer than the maximum domain length.
        """
        if len(processed_value) > self._DOMAIN_MAX_DOMAIN_LENGTH:
            self._raise_value_has_not_valid_domain_length(value=value)

    def _raise_value_has_not_valid_domain_length(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value has not a valid domain length.

        Args:
            value (str): The invalid domain value.

        Raises:
            ValueError: If the value has not a valid domain length.
        """
        raise ValueError(f'DomainValueObject value <<<{value}>>> length is longer than <<<{self._DOMAIN_MAX_DOMAIN_LENGTH}>>> characters.')  # noqa: E501  # fmt: skip

    @validation(order=2, early_process=True)
    def _validate_domain_labels(self, value: str, processed_value: str) -> None:
        """
        Validate each label (label) according to standard DNS rules.
         - Label must be between 1 and 63 characters long.
         - Label must only contain letters, digits, or hyphens.
         - Label must not start or end with a hyphen.

        Args:
            value (str): The domain value.
            processed_value (str): The early processed value.

        Raises:
            ValueError: If value has a label shorter than the minimum length.
            ValueError: If value has a label longer than the maximum length.
            ValueError: If value has a label starting with a hyphen.
            ValueError: If value has a label ending with a hyphen.
            ValueError: If value has a label containing invalid characters.
        """
        labels = processed_value.split(sep='.')

        labels = labels[:-1] if len(labels) > 1 else labels  # remove top level domain
        for label in labels:
            if len(label) < self._DOMAIN_MIN_LABEL_LENGTH:
                self._raise_value_labels_are_shorter_than_minimum_length(value=value, label=label)

            if len(label) > self._DOMAIN_MAX_LABEL_LENGTH:
                self._raise_value_labels_are_longer_than_maximum_length(value=value, label=label)

            if label[0] == '-':
                self._raise_value_has_not_valid_format(value=value, label=label)

            if label[-1] == '-':
                self._raise_value_has_not_valid_format(value=value, label=label)

            if not self._DOMAIN_REGEX.fullmatch(string=label.encode(encoding='idna').decode(encoding='utf-8')):
                self._raise_value_has_not_valid_format(value=value, label=label)

    def _raise_value_labels_are_shorter_than_minimum_length(self, value: str, label: str) -> NoReturn:
        """
        Raises a ValueError if the value labels are shorter than the minimum length.

        Args:
            value (str): The invalid domain value.

        Raises:
            ValueError: If value has a label shorter than the minimum length.
        """
        raise ValueError(f'DomainValueObject value <<<{value}>>> has a label <<<{label}>>> shorter than <<<{self._DOMAIN_MIN_LABEL_LENGTH}>>> characters.')  # noqa: E501  # fmt: skip

    def _raise_value_labels_are_longer_than_maximum_length(self, value: str, label: str) -> NoReturn:
        """
        Raises a ValueError if the value labels are longer than the maximum length.

        Args:
            value (str): The invalid domain value.
            label (str): The label that exceeds the maximum length.

        Raises:
            ValueError: If value has a label longer than the maximum length.
        """
        raise ValueError(f'DomainValueObject value <<<{value}>>> has a label <<<{label}>>> longer than <<<{self._DOMAIN_MAX_LABEL_LENGTH}>>> characters.')  # noqa: E501  # fmt: skip

    def _raise_value_has_not_valid_format(self, value: str, label: str) -> NoReturn:
        """
        Raises a ValueError if the value has not a valid format.

        Args:
            value (str): The invalid domain value.
            label (str): The label that contains invalid characters.

        Raises:
            ValueError: If the value has not a valid format.
        """
        raise ValueError(f'DomainValueObject value <<<{value}>>> has a label <<<{label}>>> with invalid format, hyphens must be used only between letters and digits.')  # noqa: E501  # fmt: skip
