# ruff: noqa: N802
"""
Ipv6AddressValueObject value object.
"""

from __future__ import annotations

from ipaddress import AddressValueError, IPv6Address

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class Ipv6AddressValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    Ipv6AddressValueObject value object.
    """

    @process(order=0)
    def _ensure_value_is_normalized(self, value: str) -> str:
        """
        Ensures the value object value is normalized IPv6 address.

        Args:
            value (str): Value.

        Returns:
            str: Value with the normalized IPv6 address.
        """
        value = self._ipv6_normalize(value=value)
        return str(object=IPv6Address(address=value))

    @validation(order=0)
    def _ensure_value_is_valid_ipv6_address(self, value: str) -> None:
        """
        Ensures the value object value is a valid IPv6 address.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not a valid IPv6 address.
        """
        value = self._ipv6_normalize(value=value)

        try:
            IPv6Address(address=value)
        except AddressValueError as error:
            raise ValueError(f'Ipv6AddressValueObject value <<<{value}>>> is not a valid IPv6 address.') from error

    @classmethod
    def _ipv6_normalize(cls, value: str) -> str:
        """
        Normalizes the given IPv6 address.

        Args:
            value (str): IPv6 address.

        Returns:
            str: Normalized IPv6 address.
        """
        if '/' in value and value.endswith('/128'):
            value = value[:-4]

        return value

    @classmethod
    def is_reserved(cls, *, value: str) -> bool:
        """
        Checks if the given IPv6 address is reserved.

        Args:
            value (str): IPv6 address.

        Returns:
            bool: True if the given IPv6 address is reserved, False otherwise.
        """
        try:
            value = cls._ipv6_normalize(value=value)
            return IPv6Address(address=value).is_reserved
        except AddressValueError:
            return False

    @classmethod
    def is_private(cls, *, value: str) -> bool:
        """
        Checks if the given IPv6 address is private.

        Args:
            value (str): IPv6 address.

        Returns:
            bool: True if the given IPv6 address is private, False otherwise.
        """
        try:
            value = cls._ipv6_normalize(value=value)
            return IPv6Address(address=value).is_private
        except AddressValueError:
            return False

    @classmethod
    def is_global(cls, *, value: str) -> bool:
        """
        Checks if the given IPv6 address is global.

        Args:
            value (str): IPv6 address.

        Returns:
            bool: True if the given IPv6 address is global, False otherwise.
        """
        try:
            value = cls._ipv6_normalize(value=value)
            return IPv6Address(address=value).is_global
        except AddressValueError:
            return False

    @classmethod
    def is_multicast(cls, *, value: str) -> bool:
        """
        Checks if the given IPv6 address is multicast.

        Args:
            value (str): IPv6 address.

        Returns:
            bool: True if the given IPv6 address is multicast, False otherwise.
        """
        try:
            value = cls._ipv6_normalize(value=value)
            return IPv6Address(address=value).is_multicast
        except AddressValueError:
            return False

    @classmethod
    def is_unspecified(cls, *, value: str) -> bool:
        """
        Checks if the given IPv6 address is unspecified.

        Args:
            value (str): IPv6 address.

        Returns:
            bool: True if the given IPv6 address is unspecified, False otherwise.
        """
        try:
            value = cls._ipv6_normalize(value=value)
            return IPv6Address(address=value).is_unspecified
        except AddressValueError:
            return False

    @classmethod
    def is_loopback(cls, *, value: str) -> bool:
        """
        Checks if the given IPv6 address is loopback.

        Args:
            value (str): IPv6 address.

        Returns:
            bool: True if the given IPv6 address is loopback, False otherwise.
        """
        try:
            value = cls._ipv6_normalize(value=value)
            return IPv6Address(address=value).is_loopback
        except AddressValueError:
            return False

    @classmethod
    def is_link_local(cls, *, value: str) -> bool:
        """
        Checks if the given IPv6 address is link-local.

        Args:
            value (str): IPv6 address.

        Returns:
            bool: True if the given IPv6 address is link-local, False otherwise.
        """
        try:
            value = cls._ipv6_normalize(value=value)
            return IPv6Address(address=value).is_link_local
        except AddressValueError:
            return False

    @classmethod
    def NULL(cls) -> Ipv6AddressValueObject:
        """
        Returns the null IPv6 address.

        Returns:
            Ipv6AddressValueObject: Null IPv6 address.
        """
        return cls(value='::')

    @classmethod
    def LOOPBACK(cls) -> Ipv6AddressValueObject:
        """
        Returns the loopback IPv6 address.

        Returns:
            Ipv6AddressValueObject: Loopback IPv6 address.
        """
        return cls(value='::1')