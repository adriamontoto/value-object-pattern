"""
IpAddressValueObject value object.
"""

from typing import NoReturn

from value_object_pattern import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .ipv4_address_value_object import Ipv4AddressValueObject
from .ipv6_address_value_object import Ipv6AddressValueObject


class IpAddressValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    IpAddressValueObject value object ensures the provided value is a valid ip address.

    Example:
    ```python
    from value_object_pattern.usables.internet import IpAddressValueObject

    ip_address = IpAddressValueObject(value='192.168.1.1')
    print(repr(ip_address))
    # >>> IpAddressValueObject(value='192.168.1.1')
    ```
    """

    @process(order=0)
    def _ensure_ip_address_stored_respective_format(self, value: str) -> str:
        """
        Ensure ip address is stored in respective format, domain, IPv4 or IPv6 address.

        Args:
            value (str): The ip address value.

        Returns:
            str: The ip address value stored in respective format.
        """
        if self._is_ipv4_address(value=value):
            return Ipv4AddressValueObject(value=value).value

        return Ipv6AddressValueObject(value=value).value

    @validation(order=0)
    def _validate_ip_address(self, value: str) -> None:
        """
        Validate that the ip address is a domain or an IPv4 or IPv6 address.

        Args:
            value (str): The ip address value.

        Raises:
            ValueError: If the ip address is not a domain or an IPv4 or IPv6 address.
        """
        if not (self._is_ipv4_address(value=value) or self._is_ipv6_address(value=value)):
            self._raise_value_is_not_valid_ip_address(value=value)

    def _raise_value_is_not_valid_ip_address(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value is not a valid ip address.

        Args:
            value (str): The provided value.
        """
        raise ValueError(f'IpAddressValueObject value <<<{value}>>> must be an IPv4 or IPv6 address.')

    def is_ipv4_address(self) -> bool:
        """
        Checks if a value is an IPv4 ip address.

        Args:
            value (str): Value.

        Returns:
            bool: True if the value is an IPv4 ip address, False otherwise.

        Example:
        ```python
        from value_object_pattern.usables.internet import IpAddressValueObject

        ip_address = IpAddressValueObject(value='1.1.1.1')
        print(ip_address.is_ipv4_address())
        # >>> True
        ```
        """
        return self._is_ipv4_address(value=self.value)

    def _is_ipv4_address(self, value: str) -> bool:
        """
        Checks if a value is an IPv4 address.

        Args:
            value (str): Value.

        Returns:
            bool: True if the value is an IPv4 address, False otherwise.
        """
        try:
            Ipv4AddressValueObject(value=value)
            return True

        except (TypeError, ValueError):
            return False

    def is_ipv6_address(self) -> bool:
        """
        Checks if a value is an IPv6 ip address.

        Args:
            value (str): Value.

        Returns:
            bool: True if the value is an IPv6 ip address, False otherwise.

        Example:
        ```python
        from value_object_pattern.usables.internet import IpAddressValueObject

        ip_address = IpAddressValueObject(value='a1c4:c052:a98e:8da4:301a:bd2a:3b36:36b4')
        print(ip_address.is_ipv6_address())
        # >>> True
        ```
        """
        return self._is_ipv6_address(value=self.value)

    def _is_ipv6_address(self, value: str) -> bool:
        """
        Checks if a value is an IPv6 address.

        Args:
            value (str): Value.

        Returns:
            bool: True if the value is an IPv6 address, False otherwise.
        """
        try:
            Ipv6AddressValueObject(value=value)
            return True

        except (TypeError, ValueError):
            return False
