"""
HostValueObject value object.
"""

from typing import NoReturn

from value_object_pattern import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .domain_value_object import DomainValueObject
from .ipv4_address_value_object import Ipv4AddressValueObject
from .ipv6_address_value_object import Ipv6AddressValueObject


class HostValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    HostValueObject value object ensures the provided value is a valid host.

    Example:
    ```python
    from value_object_pattern.usables.internet import HostValueObject

    hostname = HostValueObject(value='github.com')
    print(repr(hostname))
    # >>> HostValueObject(value=github.com)
    ```
    """

    @process(order=0)
    def _ensure_host_stored_respective_format(self, value: str) -> str:
        """
        Ensure host is stored in respective format, domain, IPv4 or IPv6 address.

        Args:
            value (str): The host value.

        Returns:
            str: The host value stored in respective format.
        """
        if self._is_domain(value=value):
            return DomainValueObject(value=value).value

        if self._is_ipv4_address(value=value):
            return Ipv4AddressValueObject(value=value).value

        return Ipv6AddressValueObject(value=value).value

    @validation(order=0)
    def _validate_host(self, value: str) -> None:
        """
        Validate that the host is a domain or an IPv4 or IPv6 address.

        Args:
            value (str): The host value.

        Raises:
            ValueError: If the host is not a domain or an IPv4 or IPv6 address.
        """
        if not (
            self._is_domain(value=value) or \
            self._is_ipv4_address(value=value) or \
            self._is_ipv6_address(value=value)
        ):  # fmt: skip
            self._raise_value_is_not_valid_host(value=value)

    def _raise_value_is_not_valid_host(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value is not a valid host.

        Args:
            value (str): The provided value.
        """
        raise ValueError(f'HostValueObject value <<<{value}>>> must be a domain or an IPv4 or IPv6 address.')

    def is_domain(self) -> bool:
        """
        Checks if a value is a domain.

        Args:
            value (str): Value.

        Returns:
            bool: True if the value is a host, False otherwise.

        Example:
        ```python
        from value_object_pattern.usables.internet import HostValueObject

        hostname = HostValueObject(value='github.com')
        print(hostname.is_domain())
        # >>> True
        ```
        """
        return self._is_domain(value=self.value)

    def _is_domain(self, value: str) -> bool:
        """
        Checks if a value is a domain.

        Args:
            value (str): Value.

        Returns:
            bool: True if the value is a domain, False otherwise.
        """
        try:
            DomainValueObject(value=value)
            return True

        except (TypeError, ValueError):
            return False

    def is_ipv4_address(self) -> bool:
        """
        Checks if a value is an IPv4 host.

        Args:
            value (str): Value.

        Returns:
            bool: True if the value is an IPv4 host, False otherwise.

        Example:
        ```python
        from value_object_pattern.usables.internet import HostValueObject

        hostname = HostValueObject(value='1.1.1.1')
        print(hostname.is_ipv4_address())
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
        Checks if a value is an IPv6 host.

        Args:
            value (str): Value.

        Returns:
            bool: True if the value is an IPv6 host, False otherwise.

        Example:
        ```python
        from value_object_pattern.usables.internet import HostValueObject

        hostname = HostValueObject(value='a1c4:c052:a98e:8da4:301a:bd2a:3b36:36b4')
        print(hostname.is_ipv6_address())
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
