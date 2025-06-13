# ruff: noqa: N802
"""
Ipv6AddressValueObject value object.
"""

from __future__ import annotations

from ipaddress import AddressValueError, IPv6Address

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class Ipv6AddressValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    Ipv6AddressValueObject value object ensures the provided value is a valid IPv6 address.

    Example:
    ```python
    from value_object_pattern.usables.internet import Ipv6AddressValueObject

    ip = Ipv6AddressValueObject(value='e8f5:bbcf:f16d:8fc1:ab49:a3ae:36eb:b254')

    print(repr(ip))
    # >>> Ipv6AddressValueObject(value=e8f5:bbcf:f16d:8fc1:ab49:a3ae:36eb:b254)
    ```
    """

    @process(order=0)
    def _ensure_value_is_normalized(self, value: str) -> str:
        """
        Ensures the value object value is normalized IPv6 address.

        Args:
            value (str): Value.

        Returns:
            str: Value with the normalized IPv6 address.
        """
        value = self._ipv6_address_normalize(value=value)
        return str(object=self._ipv6_address_validate(value=value))

    @validation(order=0)
    def _ensure_value_is_valid_ipv6_address(self, value: str) -> None:
        """
        Ensures the value object value is a valid IPv6 address.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not a valid IPv6 address.
        """
        value = self._ipv6_address_normalize(value=value)
        self._ipv6_address_validate(value=value)

    @classmethod
    def _ipv6_address_normalize(cls, value: str) -> str:
        """
        Normalizes the given IPv6 address.

        Args:
            value (str): IPv6 address.

        Returns:
            str: Normalized IPv6 address.
        """
        if '/' in value and value.endswith('/128'):
            value = value[:-4]

        if value.startswith('[') and value.endswith(']'):
            value = value[1:-1]

        return value

    @classmethod
    def _ipv6_address_validate(cls, value: str) -> IPv6Address:
        """
        Validates the given IPv6 address.

        Args:
            value (str): IPv6 address.

        Raises:
            ValueError: If the value is not a valid IPv6 address.

        Returns:
            IPv6Address: IPv6 address.
        """
        try:
            return IPv6Address(address=value)

        except AddressValueError as error:
            raise ValueError(f'Ipv6AddressValueObject value <<<{value}>>> is not a valid IPv6 address.') from error

    def is_reserved(self) -> bool:
        """
        Checks if the given IPv6 address is reserved.

        Args:
            value (str): IPv6 address.

        Returns:
            bool: True if the given IPv6 address is reserved, False otherwise.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv6AddressValueObject

        is_reserved = Ipv6AddressValueObject(value='800::').is_reserved()

        print(is_reserved)
        # >>> True
        ```
        """
        return self._ipv6_address_validate(value=self.value).is_reserved

    def is_private(self) -> bool:
        """
        Checks if the given IPv6 address is private.

        Args:
            value (str): IPv6 address.

        Returns:
            bool: True if the given IPv6 address is private, False otherwise.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv6AddressValueObject

        is_private = Ipv6AddressValueObject(value='fd00::1').is_private()

        print(is_private)
        # >>> True
        ```
        """
        return self._ipv6_address_validate(value=self.value).is_private

    def is_global(self) -> bool:
        """
        Checks if the given IPv6 address is global.

        Args:
            value (str): IPv6 address.

        Returns:
            bool: True if the given IPv6 address is global, False otherwise.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv6AddressValueObject

        is_global = Ipv6AddressValueObject(value='e8f5:bbcf:f16d:8fc1:ab49:a3ae:36eb:b254').is_global()

        print(is_global)
        # >>> True
        ```
        """
        return self._ipv6_address_validate(value=self.value).is_global

    def is_multicast(self) -> bool:
        """
        Checks if the given IPv6 address is multicast.

        Args:
            value (str): IPv6 address.

        Returns:
            bool: True if the given IPv6 address is multicast, False otherwise.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv6AddressValueObject

        is_multicast = Ipv6AddressValueObject(value='ff02::1').is_multicast()

        print(is_multicast)
        # >>> True
        ```
        """
        return self._ipv6_address_validate(value=self.value).is_multicast

    def is_unspecified(self) -> bool:
        """
        Checks if the given IPv6 address is unspecified.

        Args:
            value (str): IPv6 address.

        Returns:
            bool: True if the given IPv6 address is unspecified, False otherwise.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv6AddressValueObject

        is_unspecified = Ipv6AddressValueObject(value='::').is_unspecified()

        print(is_unspecified)
        # >>> True
        ```
        """
        return self._ipv6_address_validate(value=self.value).is_unspecified

    def is_loopback(self) -> bool:
        """
        Checks if the given IPv6 address is loopback.

        Args:
            value (str): IPv6 address.

        Returns:
            bool: True if the given IPv6 address is loopback, False otherwise.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv6AddressValueObject

        is_loopback = Ipv6AddressValueObject(value='::1').is_loopback()

        print(is_loopback)
        # >>> True
        ```
        """
        return self._ipv6_address_validate(value=self.value).is_loopback

    def is_link_local(self) -> bool:
        """
        Checks if the given IPv6 address is link-local.

        Args:
            value (str): IPv6 address.

        Returns:
            bool: True if the given IPv6 address is link-local, False otherwise.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv6AddressValueObject

        is_link_local = Ipv6AddressValueObject(value='fe80::1').is_link_local()

        print(is_link_local)
        # >>> True
        ```
        """
        return self._ipv6_address_validate(value=self.value).is_link_local

    @classmethod
    def UNSPECIFIED(cls) -> Ipv6AddressValueObject:
        """
        Returns the unspecified IPv6 address (::).

        Returns:
            Ipv6AddressValueObject: Unspecified IPv6 address.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv6AddressValueObject

        ip = Ipv6AddressValueObject.UNSPECIFIED()

        print(repr(ip))
        # >>> Ipv6AddressValueObject(value=::)
        ```
        """
        return cls(value='::')

    @classmethod
    def LOOPBACK(cls) -> Ipv6AddressValueObject:
        """
        Returns the loopback IPv6 address (::1).

        Returns:
            Ipv6AddressValueObject: Loopback IPv6 address.

        Example:
        ```python
        from value_object_pattern.usables.internet import Ipv6AddressValueObject

        ip = Ipv6AddressValueObject.LOOPBACK()

        print(repr(ip))
        # >>> Ipv6AddressValueObject(value=::1)
        ```
        """
        return cls(value='::1')
