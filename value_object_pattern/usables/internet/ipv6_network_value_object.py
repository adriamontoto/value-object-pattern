# ruff: noqa: N802
"""
Ipv6NetworkValueObject value object.
"""

from ipaddress import IPv6Network, NetmaskValueError
from typing import Generator, NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .ipv6_address_value_object import Ipv6AddressValueObject


class Ipv6NetworkValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    Ipv6NetworkValueObject value object ensures the provided value is a valid IPv6 network.

    Example:
    ```python
    from value_object_pattern.usables.internet import Ipv6NetworkValueObject

    network = Ipv6NetworkValueObject(value='e8f5:bbcf:f16d:8fc1:ab49:a3ae:36eb:b254')
    print(repr(network))
    # >>> Ipv6NetworkValueObject(value=e8f5:bbcf:f16d:8fc1:ab49:a3ae:36eb:b254/128)
    ```
    """

    _internal_network_object: IPv6Network

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
        try:
            self._internal_network_object = IPv6Network(address=value)

        except NetmaskValueError:
            self._raise_value_has_not_a_valid_netmask(value=value)

        except Exception:
            self._raise_value_is_not_ipv6_network(value=value)

    def _raise_value_has_not_a_valid_netmask(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value does not have a valid netmask.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the value does not have a valid netmask.
        """
        raise ValueError(f'Ipv6NetworkValueObject value <<<{value}>>> has an invalid netmask.')

    def _raise_value_is_not_ipv6_network(self, value: str) -> NoReturn:
        """
        Raises a TypeError if the value is not a valid IPv6 network.

        Args:
            value (str): The provided value.

        Raises:
            TypeError: If the value is not a valid IPv6 network.
        """
        raise ValueError(f'Ipv6NetworkValueObject value <<<{value}>>> is not a valid IPv6 network.')

    def hosts(self) -> Generator[Ipv6AddressValueObject, None, None]:  # noqa: UP043
        """
        Returns an iterator over the addresses of the given IPv6 network excluding the network address. If you want to
        iterate over all the addresses including the network address, use the `all_addresses` method.

        Returns:c
            Generator[Ipv6AddressValueObject, None, None]: Iterator of IP addresses.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv6NetworkValueObject

        network = Ipv6NetworkValueObject(value='2001:db8::/124')
        for address in network.hosts():
            print(repr(address))
        # >>> Ipv6AddressValueObject(value='2001:db8::1')
        # >>> Ipv6AddressValueObject(value='2001:db8::2')
        # >>> ...
        # >>> Ipv6AddressValueObject(value='2001:db8::e')
        # >>> Ipv6AddressValueObject(value='2001:db8::f')
        ```
        """
        for address in self._internal_network_object.hosts():
            yield Ipv6AddressValueObject(value=str(object=address))

    def all_addresses(self) -> Generator[Ipv6AddressValueObject, None, None]:  # noqa: UP043
        """
        Returns an iterator over all the addresses of the given IPv6 network, including the network address. If you
        want to iterate over the addresses excluding the network address, use the `hosts` method.

        Returns:
            Generator[Ipv6AddressValueObject, None, None]: Iterator of IP addresses.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv6NetworkValueObject

        network = Ipv6NetworkValueObject(value='2001:db8::/124')
        for address in network.all_addresses():
            print(repr(address))
        # >>> Ipv6AddressValueObject(value='2001:db8::')
        # >>> Ipv6AddressValueObject(value='2001:db8::1')
        # >>> ...
        # >>> Ipv6AddressValueObject(value='2001:db8::e')
        # >>> Ipv6AddressValueObject(value='2001:db8::f')
        ```
        """
        for address in self._internal_network_object:
            yield Ipv6AddressValueObject(value=str(address))

    def get_network(self) -> Ipv6AddressValueObject:
        """
        Returns the network of the given IPv6 network.

        Args:
            value (str): IPv6 network.

        Returns:
            Ipv6AddressValueObject: The network IPv6 address.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv6NetworkValueObject

        network = Ipv6NetworkValueObject(value='fd5b:207::/48')
        print(repr(network.get_network()))
        # >>> Ipv6AddressValueObject(value=fd5b:207::)
        ```
        """
        return Ipv6AddressValueObject(value=str(object=self._internal_network_object.network_address))

    def get_mask(self) -> int:
        """
        Returns the mask of the given IPv6 network.

        Args:
            value (str): IPv6 network.

        Returns:
            int: The network mask.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv6NetworkValueObject

        network = Ipv6NetworkValueObject(value='fd5b:207::/48')
        print(network.get_mask())
        # >>> 48
        ```
        """
        return self._internal_network_object.prefixlen

    def get_number_addresses(self) -> int:
        """
        Returns the number of addresses of the given IPv6 network.

        Args:
            value (str): IPv6 network.

        Returns:
            int: The number of addresses.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv6NetworkValueObject

        network = Ipv6NetworkValueObject(value='fd5b:207::/48')
        print(network.get_number_addresses())
        # >>> 1208925819614629174706176
        ```
        """
        return self._internal_network_object.num_addresses
