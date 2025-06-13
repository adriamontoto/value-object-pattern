# ruff: noqa: N802
"""
Ipv4AddressValueObject value object.
"""

from __future__ import annotations

from ipaddress import AddressValueError, IPv4Address

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

    @process(order=0)
    def _ensure_value_is_normalized(self, value: str) -> str:
        """
        Ensures the value object value is normalized IPv4 address.

        Args:
            value (str): Value.

        Returns:
            str: Value with the normalized IPv4 address.
        """
        value = self._ipv4_address_normalize(value=value)
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
        value = self._ipv4_address_normalize(value=value)
        self._ipv4_address_validate(value=value)

    @classmethod
    def _ipv4_address_normalize(cls, value: str) -> str:
        """
        Normalizes the given IPv4 address.

        Args:
            value (str): IPv4 address.

        Returns:
            str: Normalized IPv4 address.
        """
        if '/' in value and value.endswith('/32'):
            value = value[:-3]

        return value

    @classmethod
    def _ipv4_address_validate(cls, value: str) -> IPv4Address:
        """
        Validates the given IPv4 address.

        Args:
            value (str): IPv4 address.

        Raises:
            ValueError: If the value is not a valid IPv4 address.

        Returns:
            IPv4Address: IPv4 address.
        """
        try:
            return IPv4Address(address=value)

        except AddressValueError as error:
            raise ValueError(f'Ipv4AddressValueObject value <<<{value}>>> is not a valid IPv4 address.') from error

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

        is_reserved = Ipv4AddressValueObject(value='240.0.0.0').is_reserved()

        print(is_reserved)
        # >>> True
        ```
        """
        return self._ipv4_address_validate(value=self.value).is_reserved

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

        is_private = Ipv4AddressValueObject(value='192.168.10.4').is_private()

        print(is_private)
        # >>> True
        ```
        """
        return self._ipv4_address_validate(value=self.value).is_private

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

        is_global = Ipv4AddressValueObject(value='66.162.207.81').is_global()

        print(is_global)
        # >>> True
        ```
        """
        return self._ipv4_address_validate(value=self.value).is_global

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

        is_multicast = Ipv4AddressValueObject(value='224.0.0.1').is_multicast()

        print(is_multicast)
        # >>> True
        ```
        """
        return self._ipv4_address_validate(value=self.value).is_multicast

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

        is_unspecified = Ipv4AddressValueObject(value='0.0.0.0').is_unspecified()

        print(is_unspecified)
        # >>> True
        ```
        """
        return self._ipv4_address_validate(value=self.value).is_unspecified

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

        is_loopback = Ipv4AddressValueObject(value='127.0.0.1').is_loopback()

        print(is_loopback)
        # >>> True
        ```
        """
        return self._ipv4_address_validate(value=self.value).is_loopback

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

        is_link_local = Ipv4AddressValueObject(value='169.254.0.0').is_link_local()

        print(is_link_local)
        # >>> True
        ```
        """
        return self._ipv4_address_validate(value=self.value).is_link_local

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
