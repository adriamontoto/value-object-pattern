# ruff: noqa: N802
"""
Ipv4NetworkValueObject value object.
"""

from __future__ import annotations

from ipaddress import AddressValueError, IPv4Network, NetmaskValueError

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .ipv4_address_value_object import Ipv4AddressValueObject


class Ipv4NetworkValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    Ipv4NetworkValueObject value object.
    """

    @process(order=0)
    def _ensure_value_is_normalized(self, value: str) -> str:
        """
        Ensures the value object value is normalized IPv4 network.

        Args:
            value (str): Value.

        Returns:
            str: Value with the normalized IPv4 network.
        """
        return str(object=IPv4Network(address=value))

    @validation(order=0)
    def _ensure_value_is_valid_ipv4_network(self, value: str) -> None:
        """
        Ensures the value object value is a valid IPv4 network.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not a valid IPv4 network.
        """
        self._ipv4_network_validate(value=value)

    @classmethod
    def _ipv4_network_validate(cls, value: str) -> IPv4Network:
        """
        Validates the given IPv4 network.

        Args:
            value (str): IPv4 network.

        Raises:
            ValueError: If the value is not a valid IPv4 network.
            ValueError: If the value has an invalid netmask.

        Returns:
            IPv4Network: IPv4 network.
        """
        try:
            return IPv4Network(address=value)

        except NetmaskValueError as error:
            raise ValueError(f'Ipv4NetworkValueObject value <<<{value}>>> has an invalid netmask.') from error
        except (AddressValueError, ValueError) as error:
            raise ValueError(f'Ipv4NetworkValueObject value <<<{value}>>> is not a valid IPv4 network.') from error

    @classmethod
    def get_network(cls, *, value: str) -> Ipv4AddressValueObject:
        """
        Returns the network of the given IPv4 network.

        Args:
            value (str): IPv4 network.

        Raises:
            ValueError: If the value is not a valid IPv4 network.
            ValueError: If the value has an invalid netmask.

        Returns:
            Ipv4AddressValueObject: The network IPv4 address.
        """
        return Ipv4AddressValueObject(value=str(object=cls._ipv4_network_validate(value=value).network_address))

    @classmethod
    def get_broadcast(cls, *, value: str) -> Ipv4AddressValueObject:
        """
        Returns the broadcast of the given IPv4 network.

        Args:
            value (str): IPv4 network.

        Raises:
            ValueError: If the value is not a valid IPv4 network.
            ValueError: If the value has an invalid netmask.

        Returns:
            Ipv4AddressValueObject: The broadcast IPv4 address.
        """
        return Ipv4AddressValueObject(value=str(object=cls._ipv4_network_validate(value=value).broadcast_address))

    @classmethod
    def get_mask(cls, *, value: str) -> int:
        """
        Returns the mask of the given IPv4 network.

        Args:
            value (str): IPv4 network.

        Raises:
            ValueError: If the value is not a valid IPv4 network.
            ValueError: If the value has an invalid netmask.

        Returns:
            int: The network mask.
        """
        return cls._ipv4_network_validate(value=value).prefixlen

    @classmethod
    def get_number_addresses(cls, *, value: str) -> int:
        """
        Returns the number of addresses of the given IPv4 network.

        Args:
            value (str): IPv4 network.

        Raises:
            ValueError: If the value is not a valid IPv4 network.
            ValueError: If the value has an invalid netmask.

        Returns:
            int: The number of addresses.
        """
        return cls._ipv4_network_validate(value=value).num_addresses

    @classmethod
    def is_reserved(cls, *, value: str) -> bool:
        """
        Checks if the given IPv4 network is reserved.

        Args:
            value (str): IPv4 network.

        Returns:
            bool: True if the given IPv4 network is reserved, False otherwise.
        """
        try:
            return cls._ipv4_network_validate(value=value).is_reserved

        except ValueError:
            return False

    @classmethod
    def is_private(cls, *, value: str) -> bool:
        """
        Checks if the given IPv4 network is private.

        Args:
            value (str): IPv4 network.

        Returns:
            bool: True if the given IPv4 network is private, False otherwise.
        """
        try:
            return cls._ipv4_network_validate(value=value).is_private

        except ValueError:
            return False

    @classmethod
    def is_global(cls, *, value: str) -> bool:
        """
        Checks if the given IPv4 network is global.

        Args:
            value (str): IPv4 network.

        Returns:
            bool: True if the given IPv4 network is global, False otherwise.
        """
        try:
            return cls._ipv4_network_validate(value=value).is_global

        except ValueError:
            return False

    @classmethod
    def is_multicast(cls, *, value: str) -> bool:
        """
        Checks if the given IPv4 network is multicast.

        Args:
            value (str): IPv4 network.

        Returns:
            bool: True if the given IPv4 network is multicast, False otherwise.
        """
        try:
            return cls._ipv4_network_validate(value=value).is_multicast

        except ValueError:
            return False

    @classmethod
    def is_unspecified(cls, *, value: str) -> bool:
        """
        Checks if the given IPv4 network is unspecified.

        Args:
            value (str): IPv4 network.

        Returns:
            bool: True if the given IPv4 network is unspecified, False otherwise.
        """
        try:
            return cls._ipv4_network_validate(value=value).is_unspecified

        except ValueError:
            return False

    @classmethod
    def is_loopback(cls, *, value: str) -> bool:
        """
        Checks if the given IPv4 network is loopback.

        Args:
            value (str): IPv4 network.

        Returns:
            bool: True if the given IPv4 network is loopback, False otherwise.
        """
        try:
            return cls._ipv4_network_validate(value=value).is_loopback

        except ValueError:
            return False

    @classmethod
    def is_link_local(cls, *, value: str) -> bool:
        """
        Checks if the given IPv4 network is link-local.

        Args:
            value (str): IPv4 network.

        Returns:
            bool: True if the given IPv4 network is link-local, False otherwise.
        """
        try:
            return cls._ipv4_network_validate(value=value).is_link_local

        except ValueError:
            return False

    @classmethod
    def UNSPECIFIED(cls) -> Ipv4NetworkValueObject:
        """
        Returns the unspecified IPv4 network.

        Returns:
            Ipv4NetworkValueObject: Unspecified IPv4 network.
        """
        return cls(value='0.0.0.0/0')

    @classmethod
    def LOOPBACK(cls) -> Ipv4NetworkValueObject:
        """
        Returns the loopback IPv4 network.

        Returns:
            Ipv4NetworkValueObject: Loopback IPv4 network.
        """
        return cls(value='127.0.0.1/8')
