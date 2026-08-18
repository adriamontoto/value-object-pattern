"""
Test IpNetworkValueObject value object.
"""

from object_mother_pattern.mothers.internet import (
    IpNetworkMother,
    Ipv4NetworkMother,
    Ipv6NetworkMother,
)
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.internet import IpNetworkValueObject


@mark.unit_testing
def test_ip_network_value_object_accepts_any_ip_network() -> None:
    """
    Test IpNetworkValueObject value object accepts any network values.
    """
    network = IpNetworkValueObject(value=IpNetworkMother.create())

    assert type(network.value) is str
    assert network.is_ipv4_network() or network.is_ipv6_network()


@mark.unit_testing
def test_ip_network_value_object_accepts_ipv4_network() -> None:
    """
    Test IpNetworkValueObject value object accepts IPv4 network values.
    """
    network = IpNetworkValueObject(value=Ipv4NetworkMother.create())

    assert type(network.value) is str
    assert network.is_ipv4_network()
    assert not network.is_ipv6_network()


@mark.unit_testing
def test_ip_network_value_object_accepts_ipv6_network() -> None:
    """
    Test IpNetworkValueObject value object accepts IPv6 network values.
    """
    network = IpNetworkValueObject(value=Ipv6NetworkMother.create())

    assert network.is_ipv6_network()
    assert not network.is_ipv4_network()


@mark.unit_testing
def test_ip_network_value_object_invalid_type() -> None:
    """
    Test IpNetworkValueObject value object raises ValueError when value is not an IP network.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'IpNetworkValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        IpNetworkValueObject(value=IpNetworkMother.invalid_type())


@mark.unit_testing
def test_ip_network_value_object_invalid_value() -> None:
    """
    Test IpNetworkValueObject value object raises ValueError when value is not an IP network.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'IpNetworkValueObject value <<<.*>>> must be an IPv4 or IPv6 network.',
    ):
        IpNetworkValueObject(value=IpNetworkMother.invalid_value())
