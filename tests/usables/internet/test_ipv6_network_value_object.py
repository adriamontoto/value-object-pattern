"""
Test Ipv6NetworkValueObject value object.
"""

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.internet import Ipv6NetworkValueObject


@mark.unit_testing
def test_ipv6_network_value_object_happy_path() -> None:
    """
    Test Ipv6NetworkValueObject value object happy path.
    """
    network = Ipv6NetworkValueObject(value='2001:db8::/126')

    assert type(network.value) is str
    assert network.value == '2001:db8::/126'


@mark.unit_testing
def test_ipv6_network_value_object_hosts() -> None:
    """
    Test Ipv6NetworkValueObject hosts method.
    """
    network = Ipv6NetworkValueObject(value='2001:db8::/126')

    assert [address.value for address in network.hosts()] == ['2001:db8::1', '2001:db8::2', '2001:db8::3']


@mark.unit_testing
def test_ipv6_network_value_object_all_addresses() -> None:
    """
    Test Ipv6NetworkValueObject all_addresses method.
    """
    network = Ipv6NetworkValueObject(value='2001:db8::/126')

    assert [address.value for address in network.all_addresses()] == [
        '2001:db8::',
        '2001:db8::1',
        '2001:db8::2',
        '2001:db8::3',
    ]


@mark.unit_testing
def test_ipv6_network_value_object_network_properties() -> None:
    """
    Test Ipv6NetworkValueObject network property methods.
    """
    network = Ipv6NetworkValueObject(value='2001:db8::/126')

    assert network.get_network().value == '2001:db8::'
    assert network.get_mask() == 126
    assert network.get_number_addresses() == 4


@mark.unit_testing
def test_ipv6_network_value_object_invalid_mask() -> None:
    """
    Test Ipv6NetworkValueObject value object raises ValueError when mask is invalid.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'Ipv6NetworkValueObject value <<<2001:db8::/129>>> has an invalid netmask.',
    ):
        Ipv6NetworkValueObject(value='2001:db8::/129')


@mark.unit_testing
def test_ipv6_network_value_object_invalid_address() -> None:
    """
    Test Ipv6NetworkValueObject value object raises ValueError when address is invalid.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'Ipv6NetworkValueObject value <<<not-an-ipv6-network>>> is not a valid IPv6 network.',
    ):
        Ipv6NetworkValueObject(value='not-an-ipv6-network')
