# ruff: noqa: N802
"""
Ipv4AddressValueObject value object.
"""

from __future__ import annotations

from ipaddress import IPv4Address

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class Ipv4AddressValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    Ipv4AddressValueObject value object ensures the provided value is a valid IPv4 address.

    Example:
    ```python
    from value_object_pattern.usables.internet import Ipv4AddressValueObject

    ip = Ipv4AddressValueObject(value='66.162.207.81')
    print(repr(ip))
    # >>> Ipv4AddressValueObject(value=66.162.207.81)
    ```
    """

    _internal_ip_object: IPv4Address

    @process(order=0)
    def _ensure_value_is_normalized(self, value: str) -> str:
        """
        Ensures the value object value is normalized IPv4 address.

        Args:
            value (str): Value.

        Returns:
            str: Value with the normalized IPv4 address.
        """
        if '/' in value and value.endswith('/32'):
            value = value[:-3]

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
        processed_value = self._ensure_value_is_normalized(value=value)

        try:
            self._internal_ip_object = IPv4Address(address=processed_value)

        except Exception:
            self._raise_value_is_not_valid_ipv4_address(value=value)

    def _raise_value_is_not_valid_ipv4_address(self, value: str) -> None:
        """
        Raises a ValueError if the value is not a valid IPv4 address.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not a valid IPv4 address.
        """
        raise ValueError(f'Ipv4AddressValueObject value <<<{value}>>> is not a valid IPv4 address.')

    def is_reserved(self) -> bool:
        """
        Checks if the given IPv4 address is reserved.

        Args:
            value (str): IPv4 address.

        Returns:
            bool: True if the given IPv4 address is reserved, False otherwise.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv4AddressValueObject

        ip = Ipv4AddressValueObject(value='240.0.0.0')
        print(ip.is_reserved())
        # >>> True
        ```
        """
        return self._internal_ip_object.is_reserved

    def is_private(self) -> bool:
        """
        Checks if the given IPv4 address is private.

        Args:
            value (str): IPv4 address.

        Returns:
            bool: True if the given IPv4 address is private, False otherwise.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv4AddressValueObject

        ip = Ipv4AddressValueObject(value='192.168.10.4')
        print(ip.is_private())
        # >>> True
        ```
        """
        return self._internal_ip_object.is_private

    def is_global(self) -> bool:
        """
        Checks if the given IPv4 address is global.

        Args:
            value (str): IPv4 address.

        Returns:
            bool: True if the given IPv4 address is global, False otherwise.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv4AddressValueObject

        ip = Ipv4AddressValueObject(value='66.162.207.81')
        print(ip.is_global())
        # >>> True
        ```
        """
        return self._internal_ip_object.is_global

    def is_multicast(self) -> bool:
        """
        Checks if the given IPv4 address is multicast.

        Args:
            value (str): IPv4 address.

        Returns:
            bool: True if the given IPv4 address is multicast, False otherwise.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv4AddressValueObject

        ip = Ipv4AddressValueObject(value='224.0.0.1')
        print(ip.is_multicast())
        # >>> True
        ```
        """
        return self._internal_ip_object.is_multicast

    def is_unspecified(self) -> bool:
        """
        Checks if the given IPv4 address is unspecified.

        Args:
            value (str): IPv4 address.

        Returns:
            bool: True if the given IPv4 address is unspecified, False otherwise.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv4AddressValueObject

        ip = Ipv4AddressValueObject(value='0.0.0.0')
        print(ip.is_unspecified())
        # >>> True
        ```
        """
        return self._internal_ip_object.is_unspecified

    def is_loopback(self) -> bool:
        """
        Checks if the given IPv4 address is loopback.

        Args:
            value (str): IPv4 address.

        Returns:
            bool: True if the given IPv4 address is loopback, False otherwise.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv4AddressValueObject

        ip = Ipv4AddressValueObject(value='127.0.0.1')
        print(ip.is_loopback())
        # >>> True
        ```
        """
        return self._internal_ip_object.is_loopback

    def is_link_local(self) -> bool:
        """
        Checks if the given IPv4 address is link-local.

        Args:
            value (str): IPv4 address.

        Returns:
            bool: True if the given IPv4 address is link-local, False otherwise.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv4AddressValueObject

        ip = Ipv4AddressValueObject(value='169.254.0.0')
        print(ip.is_link_local())
        # >>> True
        ```
        """
        return self._internal_ip_object.is_link_local

    @classmethod
    def UNSPECIFIED(cls) -> Ipv4AddressValueObject:
        """
        Returns the unspecified IPv4 address (0.0.0.0).

        Returns:
            Ipv4AddressValueObject: Unspecified IPv4 address.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv4AddressValueObject

        ip = Ipv4AddressValueObject.UNSPECIFIED()
        print(repr(ip))
        # >>> Ipv4AddressValueObject(value=0.0.0.0)
        ```
        """
        return cls(value='0.0.0.0')  # noqa: S104

    @classmethod
    def LOOPBACK(cls) -> Ipv4AddressValueObject:
        """
        Returns the loopback IPv4 address (127.0.0.1).

        Returns:
            Ipv4AddressValueObject: Loopback IPv4 address.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv4AddressValueObject

        ip = Ipv4AddressValueObject.LOOPBACK()
        print(repr(ip))
        # >>> Ipv4AddressValueObject(value=127.0.0.1)
        ```
        """
        return cls(value='127.0.0.1')

    @classmethod
    def BROADCAST(cls) -> Ipv4AddressValueObject:
        """
        Returns the broadcast IPv4 address (255.255.255.255).

        Returns:
            Ipv4AddressValueObject: Broadcast IPv4 address.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv4AddressValueObject

        ip = Ipv4AddressValueObject.BROADCAST()
        print(repr(ip))
        # >>> Ipv4AddressValueObject(value=255.255.255.255)
        ```
        """
        return cls(value='255.255.255.255')
