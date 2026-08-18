"""
IpNetworkValueObject value object.
"""

from typing import NoReturn

from value_object_pattern import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .ipv4_network_value_object import Ipv4NetworkValueObject
from .ipv6_network_value_object import Ipv6NetworkValueObject


class IpNetworkValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    IpNetworkValueObject value object ensures the provided value is a valid IPv4 or IPv6 network.

    Example:
    ```python
    from value_object_pattern.usables.internet import IpNetworkValueObject

    network = IpNetworkValueObject(value='192.168.1.0/24')
    print(repr(network))
    # >>> IpNetworkValueObject(value='192.168.1.0/24')
    ```
    """

    @process(order=0)
    def _ensure_ip_network_stored_respective_format(self, value: str) -> str:
        """
        Ensure the IP network is stored in its respective IPv4 or IPv6 format.

        Args:
            value (str): The IP network value.

        Returns:
            str: The IP network value stored in its respective format.
        """
        if self._is_ipv4_network(value=value):
            return Ipv4NetworkValueObject(value=value).value

        return Ipv6NetworkValueObject(value=value).value

    @validation(order=0)
    def _validate_ip_network(self, value: str) -> None:
        """
        Validate that the IP network is an IPv4 or IPv6 network.

        Args:
            value (str): The IP network value.

        Raises:
            ValueError: If the IP network is not an IPv4 or IPv6 network.
        """
        if not (self._is_ipv4_network(value=value) or self._is_ipv6_network(value=value)):
            self._raise_value_is_not_valid_ip_network(value=value)

    def _raise_value_is_not_valid_ip_network(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value is not a valid IP network.

        Args:
            value (str): The provided value.
        """
        raise ValueError(f'IpNetworkValueObject value <<<{value}>>> must be an IPv4 or IPv6 network.')

    def is_ipv4_network(self) -> bool:
        """
        Checks if the value is an IPv4 network.

        Returns:
            bool: True if the value is an IPv4 network, False otherwise.

        Example:
        ```python
        from value_object_pattern.usables.internet import IpNetworkValueObject

        network = IpNetworkValueObject(value='192.168.1.0/24')
        print(network.is_ipv4_network())
        # >>> True
        ```
        """
        return self._is_ipv4_network(value=self.value)

    def _is_ipv4_network(self, value: str) -> bool:
        """
        Checks if a value is an IPv4 network.

        Args:
            value (str): Value.

        Returns:
            bool: True if the value is an IPv4 network, False otherwise.
        """
        try:
            Ipv4NetworkValueObject(value=value)
            return True

        except (TypeError, ValueError):
            return False

    def is_ipv6_network(self) -> bool:
        """
        Checks if the value is an IPv6 network.

        Returns:
            bool: True if the value is an IPv6 network, False otherwise.

        Example:
        ```python
        from value_object_pattern.usables.internet import IpNetworkValueObject

        network = IpNetworkValueObject(value='2001:db8::/126')
        print(network.is_ipv6_network())
        # >>> True
        ```
        """
        return self._is_ipv6_network(value=self.value)

    def _is_ipv6_network(self, value: str) -> bool:
        """
        Checks if a value is an IPv6 network.

        Args:
            value (str): Value.

        Returns:
            bool: True if the value is an IPv6 network, False otherwise.
        """
        try:
            Ipv6NetworkValueObject(value=value)
            return True

        except (TypeError, ValueError):
            return False
