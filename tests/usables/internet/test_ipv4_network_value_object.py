"""
Test Ipv4NetworkValueObject value object.
"""

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.internet import Ipv4NetworkValueObject


@mark.unit_testing
def test_ipv4_network_value_object_happy_path() -> None:
    """
    Test Ipv4NetworkValueObject value object happy path.
    """
    network = Ipv4NetworkValueObject(value='192.168.0.0/30')

    assert type(network.value) is str
    assert network.value == '192.168.0.0/30'


@mark.unit_testing
def test_ipv4_network_value_object_hosts() -> None:
    """
    Test Ipv4NetworkValueObject hosts method.
    """
    network = Ipv4NetworkValueObject(value='192.168.0.0/30')

    assert [address.value for address in network.hosts()] == ['192.168.0.1', '192.168.0.2']


@mark.unit_testing
def test_ipv4_network_value_object_all_addresses() -> None:
    """
    Test Ipv4NetworkValueObject all_addresses method.
    """
    network = Ipv4NetworkValueObject(value='192.168.0.0/30')

    assert [address.value for address in network.all_addresses()] == [
        '192.168.0.0',
        '192.168.0.1',
        '192.168.0.2',
        '192.168.0.3',
    ]


@mark.unit_testing
def test_ipv4_network_value_object_network_properties() -> None:
    """
    Test Ipv4NetworkValueObject network property methods.
    """
    network = Ipv4NetworkValueObject(value='192.168.0.0/30')

    assert network.get_network().value == '192.168.0.0'
    assert network.get_broadcast().value == '192.168.0.3'
    assert network.get_mask() == 30
    assert network.get_number_addresses() == 4


@mark.unit_testing
def test_ipv4_network_value_object_invalid_mask() -> None:
    """
    Test Ipv4NetworkValueObject value object raises ValueError when mask is invalid.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'Ipv4NetworkValueObject value <<<192.168.0.0/33>>> has an invalid netmask.',
    ):
        Ipv4NetworkValueObject(value='192.168.0.0/33')


@mark.unit_testing
def test_ipv4_network_value_object_invalid_address() -> None:
    """
    Test Ipv4NetworkValueObject value object raises ValueError when address is invalid.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'Ipv4NetworkValueObject value <<<999.0.0.0/24>>> is not a valid IPv4 network.',
    ):
        Ipv4NetworkValueObject(value='999.0.0.0/24')
