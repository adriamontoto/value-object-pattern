"""
Test IpAddressValueObject value object.
"""

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.internet import IpAddressValueObject


@mark.unit_testing
def test_ip_address_value_object_accepts_ipv4_address() -> None:
    """
    Test IpAddressValueObject value object accepts IPv4 address values.
    """
    ip_address = IpAddressValueObject(value='192.168.0.1')

    assert type(ip_address.value) is str
    assert ip_address.is_ipv4_address()
    assert not ip_address.is_ipv6_address()


@mark.unit_testing
def test_ip_address_value_object_accepts_ipv6_address() -> None:
    """
    Test IpAddressValueObject value object accepts IPv6 address values.
    """
    ip_address = IpAddressValueObject(value='2001:db8::1')

    assert ip_address.is_ipv6_address()
    assert not ip_address.is_ipv4_address()


@mark.unit_testing
def test_ip_address_value_object_invalid_value() -> None:
    """
    Test IpAddressValueObject value object raises ValueError when value is not an IP address.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'IpAddressValueObject value <<<example.com>>> must be an IPv4 or IPv6 address.',
    ):
        IpAddressValueObject(value='example.com')
