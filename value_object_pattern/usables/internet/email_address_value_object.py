"""
EmailAddressValueObject value object.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn

from value_object_pattern import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .domain_value_object import DomainValueObject


class EmailAddressValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    EmailAddressValueObject value object ensures the provided value is a valid email address.

    References:
        RFC 5322: https://datatracker.ietf.org/doc/html/rfc5322

    Example:
    ```python
    from value_object_pattern.usables.internet import EmailAddressValueObject

    email = EmailAddressValueObject(value='user.name+tag@EXAMPLE.com')

    print(repr(email))
    # >>> EmailAddressValueObject(value=user.name+tag@example.com)
    ```
    """

    _EMAIL_ADDRESS_MIN_LENGTH: int = 6
    _EMAIL_ADDRESS_MAX_LENGTH: int = 320
    _EMAIL_ADDRESS_LOCAL_PART_MIN_LENGTH: int = 1
    _EMAIL_ADDRESS_LOCAL_PART_MAX_LENGTH: int = 64
    _EMAIL_ADDRESS_LOCAL_PART_REGEX: Pattern[str] = re_compile('^[!#$%&\'*+/=?^_`{|}~0-9A-Za-z-]+(?:\\.[!#$%&\'*+/=?^_`{|}~0-9A-Za-z-]+)*')  # noqa: E501  # fmt: skip
    _EMAIL_ADDRESS_DOMAIN_PART_REGEX: Pattern[str] = re_compile('^(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)(?:\\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*$')  # noqa: E501  # fmt: skip

    _internal_local_part: str
    _internal_domain_part: str

    @process(order=0)
    def _ensure_email_is_in_lowercase(self, value: str) -> str:
        """
        Ensure email is in lowercase.

        Args:
            value (str): The email value.

        Returns:
            str: The email value in lowercase.
        """
        return f'{self._internal_local_part.lower()}@{self._internal_domain_part}'

    @validation(order=0)
    def _validate_email_length(self, value: str) -> None:
        """
        Validate email length.

        Args:
            value (str): The email value.

        Raises:
            ValueError: If the value length is less than the minimum allowed.
            ValueError: If the value length is greater than the maximum allowed.
        """
        if len(value) < self._EMAIL_ADDRESS_MIN_LENGTH:
            self._raise_value_minimum_length_error(value=value, min_length=self._EMAIL_ADDRESS_MIN_LENGTH)

        if len(value) > self._EMAIL_ADDRESS_MAX_LENGTH:
            self._raise_value_maximum_length_error(value=value, max_length=self._EMAIL_ADDRESS_MAX_LENGTH)

    def _raise_value_minimum_length_error(self, value: str, min_length: int) -> NoReturn:
        """
        Raise a minimum length error for the email address value.

        Args:
            value (str): The email address value.
            min_length (int): The minimum length required.

        Raises:
            ValueError: If the value length is less than the minimum allowed.
        """
        raise ValueError(f'EmailAddressValueObject value <<<{value}>>> must be at least <<<{min_length}>>> characters long. Got <<<{len(value)}>>> characters.')  # noqa: E501 # fmt: skip

    def _raise_value_maximum_length_error(self, value: str, max_length: int) -> NoReturn:
        """
        Raise a maximum length error for the email address value.

        Args:
            value (str): The email address value.
            max_length (int): The maximum length allowed.

        Raises:
            ValueError: If the value length is greater than the maximum allowed.
        """
        raise ValueError(f'EmailAddressValueObject value <<<{value}>>> must be at most <<<{max_length}>>> characters long. Got <<<{len(value)}>>> characters.')  # noqa: E501 # fmt: skip

    @validation(order=1)
    def _validate_email_local_part_length(self, value: str) -> None:
        """
        Validate email local-part length.

        Args:
            value (str): The email value.

        Raises:
            ValueError: If the local-part length is less than the minimum allowed.
            ValueError: If the local-part length is greater than the maximum allowed.
        """
        if value.count('@') != 1:
            self._raise_value_must_contain_at_symbol_error(value=value)

        self._internal_local_part, self._internal_domain_part = value.rsplit(sep='@', maxsplit=1)

        if len(self._internal_local_part) < self._EMAIL_ADDRESS_LOCAL_PART_MIN_LENGTH:
            self._raise_value_local_part_minimum_length_error(
                value=value,
                local_part=self._internal_local_part,
                min_length=self._EMAIL_ADDRESS_LOCAL_PART_MIN_LENGTH,
            )

        if len(self._internal_local_part) > self._EMAIL_ADDRESS_LOCAL_PART_MAX_LENGTH:
            self._raise_value_local_part_maximum_length_error(
                value=value,
                local_part=self._internal_local_part,
                max_length=self._EMAIL_ADDRESS_LOCAL_PART_MAX_LENGTH,
            )

    def _raise_value_must_contain_at_symbol_error(self, value: str) -> NoReturn:
        """
        Raise an error if the email address does not contain an "@" symbol.

        Args:
            value (str): The email address value.
        """
        raise ValueError(f'EmailAddressValueObject value <<<{value}>>> must contain a single "@" symbol.')

    def _raise_value_local_part_minimum_length_error(self, value: str, local_part: str, min_length: int) -> NoReturn:
        """
        Raise a minimum length error for the email address local-part value.

        Args:
            value (str): The email address local-part value.
            local_part (str): The local part of the email address.
            min_length (int): The minimum length required.

        Raises:
            ValueError: If the value length is less than the minimum allowed.
        """
        raise ValueError(f'EmailAddressValueObject value <<<{value}>>> local part <<<{local_part}>>> must be at least <<<{min_length}>>> characters long. Got <<<{len(value)}>>> characters.')  # noqa: E501 # fmt: skip

    def _raise_value_local_part_maximum_length_error(self, value: str, local_part: str, max_length: int) -> NoReturn:
        """
        Raise a maximum length error for the email address local-part value.

        Args:
            value (str): The email address local-part value.
            local_part (str): The local part of the email address.
            max_length (int): The maximum length allowed.

        Raises:
            ValueError: If the value length is greater than the maximum allowed.
        """
        raise ValueError(f'EmailAddressValueObject value <<<{value}>>> local part <<<{local_part}>>> must be at most <<<{max_length}>>> characters long. Got <<<{len(value)}>>> characters.')  # noqa: E501 # fmt: skip

    @validation(order=2)
    def _validate_email_does_not_contain_invalid_characters(self, value: str) -> None:
        """
        Validate email address does not contain invalid characters.

        Args:
            value (str): The email address value.

        Raises:
            ValueError: If the email address local part contains invalid characters.
        """
        if not self._EMAIL_ADDRESS_LOCAL_PART_REGEX.fullmatch(string=self._internal_local_part):
            self._raise_email_address_local_contains_invalid_characters_error(
                value=value,
                local_part=self._internal_local_part,
            )

    def _raise_email_address_local_contains_invalid_characters_error(self, value: str, local_part: str) -> NoReturn:
        """
        Raise an error if the email address local part contains invalid characters.

        Args:
            value (str): The email address value.
            local_part (str): The local part of the email address.

        Raises:
            EmailAddressLocalContainsInvalidCharactersError: If the local part contains invalid characters.
        """
        raise ValueError(f'EmailAddressValueObject value <<<{value}>>> local part <<<{local_part}>>> contains invalid characters.')  # noqa: E501  # fmt: skip

    @validation(order=3)
    def _validate_email_domain(self, value: str) -> None:
        """
        Validate email top-level domain.

        Args:
            value (str): The email address value.

        Raises:
            ValueError: If the email address has an invalid top-level domain.
        """
        if not self._EMAIL_ADDRESS_DOMAIN_PART_REGEX.fullmatch(string=self._internal_domain_part):
            self._raise_email_address_domain_contains_invalid_characters_error(
                value=value,
                domain_part=self._internal_domain_part,
            )

        try:
            self._internal_domain_part = DomainValueObject(value=self._internal_domain_part).value

        except Exception as exception:
            print(f'{exception}')
            self._raise_value_invalid_domain_error(value=value, domain_part=self._internal_domain_part)

    def _raise_email_address_domain_contains_invalid_characters_error(self, value: str, domain_part: str) -> NoReturn:
        """
        Raise an error if the email address domain part contains invalid characters.

        Args:
            value (str): The email address value.
            domain_part (str): The domain part of the email address.

        Raises:
            ValueError: If the domain part contains invalid characters.
        """
        raise ValueError(f'EmailAddressValueObject value <<<{value}>>> domain part <<<{domain_part}>>> contains invalid characters.')  # noqa: E501  # fmt: skip

    def _raise_value_invalid_domain_error(self, value: str, domain_part: str) -> NoReturn:
        """
        Raise an error if the email address has an invalid domain.

        Args:
            value (str): The email address value.
            domain_part (str): The domain part of the email address.

        Raises:
            ValueError: If the email address has an invalid domain.
        """
        raise ValueError(f'EmailAddressValueObject value <<<{value}>>> has an invalid domain <<<{domain_part}>>>.')
