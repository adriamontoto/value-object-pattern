"""
HostValueObject value object.
"""

from value_object_pattern import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .domain_value_object import DomainValueObject
from .ipv4_address_value_object import Ipv4AddressValueObject
from .ipv6_address_value_object import Ipv6AddressValueObject


class HostValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    HostValueObject value object.
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
        if self.is_domain(value=value):
            return DomainValueObject(value=value).value

        if self.is_ipv4_address(value=value):
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
        if not (self.is_domain(value=value) or self.is_ipv4_address(value=value) or self.is_ipv6_address(value=value)):
            raise ValueError(f'HostValueObject value <<<{value}>>> must be a domain or an IPv4 or IPv6 address.')

    @classmethod
    def is_domain(cls, *, value: str) -> bool:
        """
        Checks if a value is a domain.

        Args:
            value (str): Value.

        Returns:
            bool: True if the value is a host, False otherwise.
        """
        try:
            DomainValueObject(value=value)
            return True

        except (TypeError, ValueError):
            return False

    @classmethod
    def is_ipv4_address(cls, *, value: str) -> bool:
        """
        Checks if a value is an IPv4 host.

        Args:
            value (str): Value.

        Returns:
            bool: True if the value is an IPv4 host, False otherwise.
        """
        try:
            Ipv4AddressValueObject(value=value)
            return True

        except (TypeError, ValueError):
            return False

    @classmethod
    def is_ipv6_address(cls, *, value: str) -> bool:
        """
        Checks if a value is an IPv6 host.

        Args:
            value (str): Value.

        Returns:
            bool: True if the value is an IPv6 host, False otherwise.
        """
        try:
            Ipv6AddressValueObject(value=value)
            return True

        except (TypeError, ValueError):
            return False
