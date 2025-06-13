# ruff: noqa: N802
"""
Ipv4NetworkValueObject value object.
"""

from ipaddress import AddressValueError, IPv4Network, NetmaskValueError

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

        ip = Ipv4NetworkValueObject(value='192.168.10.0/24').get_network()

        print(repr(ip))
        # >>> Ipv4AddressValueObject(value=192.168.10.0)
        ```
        """
        return Ipv4AddressValueObject(value=str(object=self._ipv4_network_validate(value=self.value).network_address))

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

        ip = Ipv4NetworkValueObject(value='192.168.10.0/24').get_broadcast()

        print(repr(ip))
        # >>> Ipv4AddressValueObject(value=192.168.10.255)
        ```
        """
        return Ipv4AddressValueObject(value=str(object=self._ipv4_network_validate(value=self.value).broadcast_address))

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

        mask = Ipv4NetworkValueObject(value='192.168.10.0/24').get_mask()

        print(mask)
        # >>> 24
        ```
        """
        return self._ipv4_network_validate(value=self.value).prefixlen

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

        addresses = Ipv4NetworkValueObject(value='192.168.10.0/24').get_number_addresses()

        print(addresses)
        # >>> 256
        ```
        """
        return self._ipv4_network_validate(value=self.value).num_addresses
