# ruff: noqa: N802
"""
Ipv4NetworkValueObject value object.
"""

from ipaddress import IPv4Network, NetmaskValueError
from typing import Generator, NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .ipv4_address_value_object import Ipv4AddressValueObject


class Ipv4NetworkValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    Ipv4NetworkValueObject value object ensures the provided value is a valid IPv4 network.

    Example:
    ```python
    from value_object_pattern.usables.internet import Ipv4NetworkValueObject

    network = Ipv4NetworkValueObject(value='66.162.207.81')
    print(repr(network))
    # >>> Ipv4NetworkValueObject(value=66.162.207.81/32)
    ```
    """

    _internal_network_object: IPv4Network

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
            ValueError: If the value does not have a valid netmask.
            ValueError: If the value is not a valid IPv4 network.
        """
        try:
            self._internal_network_object = IPv4Network(address=value)

        except NetmaskValueError:
            self._raise_value_has_not_a_valid_netmask(value=value)

        except Exception:
            self._raise_value_is_not_ipv4_network(value=value)

    def _raise_value_has_not_a_valid_netmask(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value does not have a valid netmask.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the value does not have a valid netmask.
        """
        raise ValueError(f'Ipv4NetworkValueObject value <<<{value}>>> has an invalid netmask.')

    def _raise_value_is_not_ipv4_network(self, value: str) -> NoReturn:
        """
        Raises a TypeError if the value is not a valid IPv4 network.

        Args:
            value (str): The provided value.

        Raises:
            TypeError: If the value is not a valid IPv4 network.
        """
        raise ValueError(f'Ipv4NetworkValueObject value <<<{value}>>> is not a valid IPv4 network.')

    def hosts(self) -> Generator[Ipv4AddressValueObject, None, None]:  # noqa: UP043
        """
        Returns an iterator over the addresses of the given IPv4 network excluding the network and broadcast addresses.
        If you want to iterate over all the addresses including the network and broadcast addresses, use the
        `all_addresses` method.

        Returns:
            Generator[Ipv4AddressValueObject, None, None]: Iterator of IP addresses.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv4NetworkValueObject

        network = Ipv4NetworkValueObject(value='192.168.10.0/24')
        for address in network.hosts():
            print(repr(address))
        # >>> Ipv4AddressValueObject(value='192.168.10.1')
        # >>> Ipv4AddressValueObject(value='192.168.10.2')
        # >>> ...
        # >>> Ipv4AddressValueObject(value='192.168.10.253')
        # >>> Ipv4AddressValueObject(value='192.168.10.254')
        ```
        """
        for address in self._internal_network_object.hosts():
            yield Ipv4AddressValueObject(value=str(object=address))

    def all_addresses(self) -> Generator[Ipv4AddressValueObject, None, None]:  # noqa: UP043
        """
        Returns an iterator over all the addresses of the given IPv4 network, including the network and broadcast
        addresses. If you want to iterate over the addresses excluding the network and broadcast addresses,
        use the `hosts` method.

        Returns:
            Generator[Ipv4AddressValueObject, None, None]: Iterator of IP addresses.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv4NetworkValueObject

        network = Ipv4NetworkValueObject(value='192.168.10.0/24')
        for address in network.all_addresses():
            print(repr(address))
        # >>> Ipv4AddressValueObject(value='192.168.10.0')
        # >>> Ipv4AddressValueObject(value='192.168.10.1')
        # >>> ...
        # >>> Ipv4AddressValueObject(value='192.168.10.254')
        # >>> Ipv4AddressValueObject(value='192.168.10.255')
        ```
        """
        for address in self._internal_network_object:
            yield Ipv4AddressValueObject(value=str(address))

    def get_network(self) -> Ipv4AddressValueObject:
        """
        Returns the network of the given IPv4 network.

        Args:
            value (str): IPv4 network.

        Returns:
            Ipv4AddressValueObject: The network IPv4 address.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv4NetworkValueObject

        network = Ipv4NetworkValueObject(value='192.168.10.0/24')
        print(repr(network.get_network()))
        # >>> Ipv4AddressValueObject(value=192.168.10.0)
        ```
        """
        return Ipv4AddressValueObject(value=str(object=self._internal_network_object.network_address))

    def get_broadcast(self) -> Ipv4AddressValueObject:
        """
        Returns the broadcast of the given IPv4 network.

        Args:
            value (str): IPv4 network.

        Returns:
            Ipv4AddressValueObject: The broadcast IPv4 address.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv4NetworkValueObject

        network = Ipv4NetworkValueObject(value='192.168.10.0/24')
        print(repr(network.get_broadcast()))
        # >>> Ipv4AddressValueObject(value=192.168.10.255)
        ```
        """
        return Ipv4AddressValueObject(value=str(object=self._internal_network_object.broadcast_address))

    def get_mask(self) -> int:
        """
        Returns the mask of the given IPv4 network.

        Args:
            value (str): IPv4 network.

        Returns:
            int: The network mask.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv4NetworkValueObject

        network = Ipv4NetworkValueObject(value='192.168.10.0/24')
        print(network.get_mask())
        # >>> 24
        ```
        """
        return self._internal_network_object.prefixlen

    def get_number_addresses(self) -> int:
        """
        Returns the number of addresses of the given IPv4 network.

        Args:
            value (str): IPv4 network.

        Returns:
            int: The number of addresses.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv4NetworkValueObject

        network = Ipv4NetworkValueObject(value='192.168.10.0/24')
        print(network.get_number_addresses())
        # >>> 256
        ```
        """
        return self._internal_network_object.num_addresses
