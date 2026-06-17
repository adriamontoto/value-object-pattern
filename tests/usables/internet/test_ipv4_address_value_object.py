"""
Test Ipv4AddressValueObject value object.
"""

from typing import Any

from pytest import MonkeyPatch, mark, raises as assert_raises

from value_object_pattern.usables.internet import Ipv4AddressValueObject


@mark.unit_testing
def test_ipv4_address_value_object_happy_path() -> None:
    """
    Test Ipv4AddressValueObject value object happy path.
    """
    address = Ipv4AddressValueObject(value='127.0.0.1/32')

    assert type(address.value) is str
    assert address.value == '127.0.0.1'


@mark.unit_testing
def test_ipv4_address_value_object_classification_methods() -> None:
    """
    Test Ipv4AddressValueObject classification methods.
    """
    assert Ipv4AddressValueObject(value='240.0.0.1').is_reserved()
    assert Ipv4AddressValueObject(value='192.168.0.1').is_private()
    assert Ipv4AddressValueObject(value='8.8.8.8').is_global()
    assert Ipv4AddressValueObject(value='224.0.0.1').is_multicast()
    assert Ipv4AddressValueObject.UNSPECIFIED().is_unspecified()
    assert Ipv4AddressValueObject.LOOPBACK().is_loopback()
    assert Ipv4AddressValueObject(value='169.254.0.1').is_link_local()
    assert Ipv4AddressValueObject.BROADCAST().value == '255.255.255.255'


@mark.unit_testing
def test_ipv4_address_value_object_invalid_value() -> None:
    """
    Test Ipv4AddressValueObject value object raises ValueError when value is not a valid IPv4 address.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r"Octet 999 \(> 255\) not permitted in '999\.0\.0\.1'",
    ):
        Ipv4AddressValueObject(value='999.0.0.1')


@mark.unit_testing
def test_ipv4_address_value_object_raises_invalid_ipv4_address() -> None:
    """
    Test Ipv4AddressValueObject defensive invalid-address error branch.
    """
    address: Any = Ipv4AddressValueObject(value='127.0.0.1')

    with assert_raises(
        expected_exception=ValueError,
        match=r'Ipv4AddressValueObject value <<<999.0.0.1>>> is not a valid IPv4 address.',
    ):
        address._raise_value_is_not_valid_ipv4_address(value='999.0.0.1')


@mark.unit_testing
def test_ipv4_address_value_object_rejects_invalid_normalized_value(monkeypatch: MonkeyPatch) -> None:
    """
    Test Ipv4AddressValueObject defensive validation branch for invalid normalized values.
    """
    address: Any = Ipv4AddressValueObject(value='127.0.0.1')

    monkeypatch.setattr(Ipv4AddressValueObject, '_ensure_value_is_normalized', lambda self, value: '999.0.0.1')

    with assert_raises(
        expected_exception=ValueError,
        match=r'Ipv4AddressValueObject value <<<invalid-ipv4>>> is not a valid IPv4 address.',
    ):
        address._ensure_value_is_valid_ipv4_address(value='invalid-ipv4')
