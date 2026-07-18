"""
Test HostValueObject value object.
"""

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.internet import HostValueObject


@mark.unit_testing
def test_host_value_object_accepts_domain() -> None:
    """
    Test HostValueObject value object accepts domain values.
    """
    host = HostValueObject(value='Example.COM')

    assert type(host.value) is str
    assert host.value == 'example.com'
    assert host.is_domain()
    assert not host.is_ipv4_address()
    assert not host.is_ipv6_address()


@mark.unit_testing
def test_host_value_object_accepts_localhost() -> None:
    """
    Test HostValueObject value object accepts and normalizes localhost.
    """
    host = HostValueObject(value='LOCALHOST.')

    assert host.value == 'localhost'
    assert host.is_domain()
    assert not host.is_ipv4_address()
    assert not host.is_ipv6_address()


@mark.unit_testing
def test_host_value_object_accepts_ipv4_address() -> None:
    """
    Test HostValueObject value object accepts IPv4 address values.
    """
    assert HostValueObject(value='192.168.0.1').is_ipv4_address()


@mark.unit_testing
def test_host_value_object_accepts_ipv6_address() -> None:
    """
    Test HostValueObject value object accepts IPv6 address values.
    """
    assert HostValueObject(value='2001:db8::1').is_ipv6_address()


@mark.unit_testing
def test_host_value_object_invalid_value() -> None:
    """
    Test HostValueObject value object raises ValueError when value is not a valid host.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'HostValueObject value <<<not_a_host>>> must be a domain or an IPv4 or IPv6 address.',
    ):
        HostValueObject(value='not_a_host')
