# ruff: noqa: N802
"""
Ipv6NetworkValueObject value object.
"""

from ipaddress import AddressValueError, IPv6Network, NetmaskValueError

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

        ip = Ipv6NetworkValueObject(value='fd5b:207::/48').get_network()

        print(repr(ip))
        # >>> Ipv6AddressValueObject(value=fd5b:207::)
        ```
        """
        return Ipv6AddressValueObject(value=str(object=self._ipv6_network_validate(value=self.value).network_address))

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

        mask = Ipv6NetworkValueObject(value='fd5b:207::/48').get_mask()

        print(mask)
        # >>> 48
        ```
        """
        return self._ipv6_network_validate(value=self.value).prefixlen

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

        addresses = Ipv6NetworkValueObject(value='fd5b:207::/48').get_number_addresses()

        print(addresses)
        # >>> 1208925819614629174706176
        ```
        """
        return self._ipv6_network_validate(value=self.value).num_addresses

    # TODO: def get_addresses(self) -> list[Ipv6AddressValueObject]:
