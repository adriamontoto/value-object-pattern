# ruff: noqa: N802
"""
Ipv4AddressValueObject value object.
"""

from __future__ import annotations

from ipaddress import AddressValueError, IPv4Address

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class Ipv4AddressValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    Ipv4AddressValueObject value object.
    """

    @process(order=0)
    def _ensure_value_is_normalized(self, value: str) -> str:
        """
        Ensures the value object value is normalized IPv4 address.

        Args:
            value (str): Value.

        Returns:
            str: Value with the normalized IPv4 address.
        """
        value = self._ipv4_normalize(value=value)
        return str(object=IPv4Address(address=value))

    @validation(order=0)
    def _ensure_value_is_valid_ipv4_address(self, value: str) -> None:
        """
        Ensures the value object value is a valid IPv4 address.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not a valid IPv4 address.
        """
        value = self._ipv4_normalize(value=value)

        try:
            IPv4Address(address=value)
        except AddressValueError as error:
            raise ValueError(f'Ipv4AddressValueObject value <<<{value}>>> is not a valid IPv4 address.') from error

    @classmethod
    def _ipv4_normalize(cls, value: str) -> str:
        """
        Normalizes the given IPv4 address.

        Args:
            value (str): IPv4 address.

        Returns:
            str: Normalized IPv4 address.
        """
        if '/' in value and value.endswith('/32'):
            value = value[:-3]

        return value

    @classmethod
    def is_reserved(cls, *, value: str) -> bool:
        """
        Checks if the given IPv4 address is reserved.

        Args:
            value (str): IPv4 address.

        Returns:
            bool: True if the given IPv4 address is reserved, False otherwise.
        """
        try:
            value = cls._ipv4_normalize(value=value)
            return IPv4Address(address=value).is_reserved
        except AddressValueError:
            return False

    @classmethod
    def is_private(cls, *, value: str) -> bool:
        """
        Checks if the given IPv4 address is private.

        Args:
            value (str): IPv4 address.

        Returns:
            bool: True if the given IPv4 address is private, False otherwise.
        """
        try:
            value = cls._ipv4_normalize(value=value)
            return IPv4Address(address=value).is_private
        except AddressValueError:
            return False

    @classmethod
    def is_global(cls, *, value: str) -> bool:
        """
        Checks if the given IPv4 address is global.

        Args:
            value (str): IPv4 address.

        Returns:
            bool: True if the given IPv4 address is global, False otherwise.
        """
        try:
            value = cls._ipv4_normalize(value=value)
            return IPv4Address(address=value).is_global
        except AddressValueError:
            return False

    @classmethod
    def is_multicast(cls, *, value: str) -> bool:
        """
        Checks if the given IPv4 address is multicast.

        Args:
            value (str): IPv4 address.

        Returns:
            bool: True if the given IPv4 address is multicast, False otherwise.
        """
        try:
            value = cls._ipv4_normalize(value=value)
            return IPv4Address(address=value).is_multicast
        except AddressValueError:
            return False

    @classmethod
    def is_unspecified(cls, *, value: str) -> bool:
        """
        Checks if the given IPv4 address is unspecified.

        Args:
            value (str): IPv4 address.

        Returns:
            bool: True if the given IPv4 address is unspecified, False otherwise.
        """
        try:
            value = cls._ipv4_normalize(value=value)
            return IPv4Address(address=value).is_unspecified
        except AddressValueError:
            return False

    @classmethod
    def is_loopback(cls, *, value: str) -> bool:
        """
        Checks if the given IPv4 address is loopback.

        Args:
            value (str): IPv4 address.

        Returns:
            bool: True if the given IPv4 address is loopback, False otherwise.
        """
        try:
            value = cls._ipv4_normalize(value=value)
            return IPv4Address(address=value).is_loopback
        except AddressValueError:
            return False

    @classmethod
    def is_link_local(cls, *, value: str) -> bool:
        """
        Checks if the given IPv4 address is link-local.

        Args:
            value (str): IPv4 address.

        Returns:
            bool: True if the given IPv4 address is link-local, False otherwise.
        """
        try:
            value = cls._ipv4_normalize(value=value)
            return IPv4Address(address=value).is_link_local
        except AddressValueError:
            return False

    @classmethod
    def NULL(cls) -> Ipv4AddressValueObject:
        """
        Returns the null IPv4 address.

        Returns:
            Ipv4AddressValueObject: Null IPv4 address.
        """
        return cls(value='0.0.0.0')

    @classmethod
    def UNSPECIFIED(cls) -> Ipv4AddressValueObject:
        """
        Returns the unspecified IPv4 address.

        Returns:
            Ipv4AddressValueObject: Unspecified IPv4 address.
        """
        return cls(value='0.0.0.0')

    @classmethod
    def LOOPBACK(cls) -> Ipv4AddressValueObject:
        """
        Returns the loopback IPv4 address.

        Returns:
            Ipv4AddressValueObject: Loopback IPv4 address.
        """
        return cls(value='127.0.0.1')

    @classmethod
    def BROADCAST(cls) -> Ipv4AddressValueObject:
        """
        Returns the broadcast IPv4 address.

        Returns:
            Ipv4AddressValueObject: Broadcast IPv4 address.
        """
        return cls(value='255.255.255.255')
