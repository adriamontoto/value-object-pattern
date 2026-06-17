"""
Test PortValueObject value object.
"""

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.internet import PortValueObject


@mark.unit_testing
def test_port_value_object_lower_bound() -> None:
    """
    Test PortValueObject value object lower bound.
    """
    assert PortValueObject(value=0).value == 0


@mark.unit_testing
def test_port_value_object_upper_bound() -> None:
    """
    Test PortValueObject value object upper bound.
    """
    assert PortValueObject(value=65535).value == 65535


@mark.unit_testing
def test_port_value_object_port_ranges() -> None:
    """
    Test PortValueObject range constructors.
    """
    assert [port.value for port in PortValueObject.system_ports()] == [0, 1023]
    assert [port.value for port in PortValueObject.user_ports()] == [1024, 49151]
    assert [port.value for port in PortValueObject.ephemeral_ports()] == [1024, 65535]


@mark.unit_testing
def test_port_value_object_named_ports() -> None:
    """
    Test PortValueObject named port constructors.
    """
    expected_ports = {
        'FTP_DATA': 20,
        'FTP_CONTROL': 21,
        'SSH': 22,
        'TELNET': 23,
        'SMTP': 25,
        'DNS': 53,
        'DHCP_SERVER': 67,
        'DHCP_CLIENT': 68,
        'HTTP': 80,
        'POP3': 110,
        'NTP': 123,
        'IMAP': 143,
        'SNMP_MONITOR': 161,
        'SNMP_TRAP': 162,
        'LDAP': 389,
        'HTTPS': 443,
        'DoH': 443,
        'SMTPS': 465,
        'DoT': 853,
        'IMAPS': 993,
        'POP3S': 995,
        'OPENVPN': 1194,
        'MICROSOFT_SQL_SERVER': 1433,
        'ORACLE': 1521,
        'MYSQL': 3306,
        'MARIADB': 3306,
        'RDP': 3389,
        'POSTGRESQL': 5432,
        'REDIS': 6379,
        'MINECRAFT': 25565,
        'MONGODB': 27017,
        'WIREGUARD': 51820,
    }

    for method_name, expected_value in expected_ports.items():
        assert getattr(PortValueObject, method_name)().value == expected_value


@mark.unit_testing
def test_port_value_object_below_lower_bound() -> None:
    """
    Test PortValueObject value object raises ValueError when value is below lower bound.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'PortValueObject value <<<-1>>> must be between 0 and 65535.',
    ):
        PortValueObject(value=-1)


@mark.unit_testing
def test_port_value_object_above_upper_bound() -> None:
    """
    Test PortValueObject value object raises ValueError when value is above upper bound.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'PortValueObject value <<<65536>>> must be between 0 and 65535.',
    ):
        PortValueObject(value=65536)
