# ruff: noqa: N802
"""
Ipv6NetworkValueObject value object.
"""

from __future__ import annotations

from ipaddress import AddressValueError, IPv6Network, NetmaskValueError

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .ipv6_address_value_object import Ipv6AddressValueObject


class Ipv6NetworkValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    Ipv6NetworkValueObject value object.
    """

    @process(order=0)
    def _ensure_value_is_normalized(self, value: str) -> str:
        """
        Ensures the value object value is normalized IPv6 network.

        Args:
            value (str): Value.

        Returns:
            str: Value with the normalized IPv6 network.
        """
        return str(object=IPv6Network(address=value))

    @validation(order=0)
    def _ensure_value_is_valid_ipv6_network(self, value: str) -> None:
        """
        Ensures the value object value is a valid IPv6 network.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not a valid IPv6 network.
        """
        self._ipv6_network_validate(value=value)

    @classmethod
    def _ipv6_network_validate(cls, value: str) -> IPv6Network:
        """
        Validates the given IPv6 network.

        Args:
            value (str): IPv6 network.

        Raises:
            ValueError: If the value is not a valid IPv6 network.
            ValueError: If the value has an invalid netmask.

        Returns:
            IPv6Network: IPv6 network.
        """
        try:
            return IPv6Network(address=value)

        except NetmaskValueError as error:
            raise ValueError(f'Ipv6NetworkValueObject value <<<{value}>>> has an invalid netmask.') from error
        except (AddressValueError, ValueError) as error:
            raise ValueError(f'Ipv6NetworkValueObject value <<<{value}>>> is not a valid IPv6 network.') from error

    @classmethod
    def get_network(cls, *, value: str) -> Ipv6AddressValueObject:
        """
        Returns the network of the given IPv6 network.

        Args:
            value (str): IPv6 network.

        Raises:
            ValueError: If the value is not a valid IPv6 network.
            ValueError: If the value has an invalid netmask.

        Returns:
            Ipv6AddressValueObject: The network IPv6 address.
        """
        return Ipv6AddressValueObject(value=str(object=cls._ipv6_network_validate(value=value).network_address))

    @classmethod
    def get_mask(cls, *, value: str) -> int:
        """
        Returns the mask of the given IPv6 network.

        Args:
            value (str): IPv6 network.

        Raises:
            ValueError: If the value is not a valid IPv6 network.
            ValueError: If the value has an invalid netmask.

        Returns:
            int: The network mask.
        """
        return cls._ipv6_network_validate(value=value).prefixlen

    @classmethod
    def get_number_addresses(cls, *, value: str) -> int:
        """
        Returns the number of addresses of the given IPv6 network.

        Args:
            value (str): IPv6 network.

        Raises:
            ValueError: If the value is not a valid IPv6 network.
            ValueError: If the value has an invalid netmask.

        Returns:
            int: The number of addresses.
        """
        return cls._ipv6_network_validate(value=value).num_addresses

    @classmethod
    def is_reserved(cls, *, value: str) -> bool:
        """
        Checks if the given IPv6 network is reserved.

        Args:
            value (str): IPv6 network.

        Returns:
            bool: True if the given IPv6 network is reserved, False otherwise.
        """
        try:
            return cls._ipv6_network_validate(value=value).is_reserved
        except AddressValueError:
            return False

    @classmethod
    def is_private(cls, *, value: str) -> bool:
        """
        Checks if the given IPv6 network is private.

        Args:
            value (str): IPv6 network.

        Returns:
            bool: True if the given IPv6 network is private, False otherwise.
        """
        try:
            return cls._ipv6_network_validate(value=value).is_private
        except ValueError:
            return False

    @classmethod
    def is_global(cls, *, value: str) -> bool:
        """
        Checks if the given IPv6 network is global.

        Args:
            value (str): IPv6 network.

        Returns:
            bool: True if the given IPv6 network is global, False otherwise.
        """
        try:
            return cls._ipv6_network_validate(value=value).is_global
        except ValueError:
            return False

    @classmethod
    def is_multicast(cls, *, value: str) -> bool:
        """
        Checks if the given IPv6 network is multicast.

        Args:
            value (str): IPv6 network.

        Returns:
            bool: True if the given IPv6 network is multicast, False otherwise.
        """
        try:
            return cls._ipv6_network_validate(value=value).is_multicast
        except ValueError:
            return False

    @classmethod
    def is_unspecified(cls, *, value: str) -> bool:
        """
        Checks if the given IPv6 network is unspecified.

        Args:
            value (str): IPv6 network.

        Returns:
            bool: True if the given IPv6 network is unspecified, False otherwise.
        """
        try:
            return cls._ipv6_network_validate(value=value).is_unspecified
        except ValueError:
            return False

    @classmethod
    def is_loopback(cls, *, value: str) -> bool:
        """
        Checks if the given IPv6 network is loopback.

        Args:
            value (str): IPv6 network.

        Returns:
            bool: True if the given IPv6 network is loopback, False otherwise.
        """
        try:
            return cls._ipv6_network_validate(value=value).is_loopback
        except ValueError:
            return False

    @classmethod
    def is_link_local(cls, *, value: str) -> bool:
        """
        Checks if the given IPv6 network is link-local.

        Args:
            value (str): IPv6 network.

        Returns:
            bool: True if the given IPv6 network is link-local, False otherwise.
        """
        try:
            return cls._ipv6_network_validate(value=value).is_link_local
        except ValueError:
            return False

    @classmethod
    def UNSPECIFIED(cls) -> Ipv6NetworkValueObject:
        """
        Returns the unspecified IPv6 network.

        Returns:
            Ipv6NetworkValueObject: Unspecified IPv6 network.
        """
        return cls(value='::/128')

    @classmethod
    def LOOPBACK(cls) -> Ipv6NetworkValueObject:
        """
        Returns the loopback IPv6 network.

        Returns:
            Ipv6NetworkValueObject: Loopback IPv6 network.
        """
        return cls(value='::1/128')
