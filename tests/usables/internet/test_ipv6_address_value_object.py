"""
Test Ipv6AddressValueObject value object.
"""

from typing import Any

from pytest import MonkeyPatch, mark, raises as assert_raises

from value_object_pattern.usables.internet import Ipv6AddressValueObject


@mark.unit_testing
def test_ipv6_address_value_object_happy_path() -> None:
    """
    Test Ipv6AddressValueObject value object happy path.
    """
    address = Ipv6AddressValueObject(value='[::1]')

    assert type(address.value) is str
    assert address.value == '::1'
    assert Ipv6AddressValueObject(value='::1/128').value == '::1'


@mark.unit_testing
def test_ipv6_address_value_object_classification_methods() -> None:
    """
    Test Ipv6AddressValueObject classification methods.
    """
    assert Ipv6AddressValueObject(value='100::').is_reserved()
    assert Ipv6AddressValueObject(value='fd00::1').is_private()
    assert Ipv6AddressValueObject(value='2001:4860:4860::8888').is_global()
    assert Ipv6AddressValueObject(value='ff02::1').is_multicast()
    assert Ipv6AddressValueObject.UNSPECIFIED().is_unspecified()
    assert Ipv6AddressValueObject.LOOPBACK().is_loopback()
    assert Ipv6AddressValueObject(value='fe80::1').is_link_local()


@mark.unit_testing
def test_ipv6_address_value_object_invalid_value() -> None:
    """
    Test Ipv6AddressValueObject value object raises ValueError when value is not a valid IPv6 address.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r"At least 3 parts expected in 'not-an-ipv6-address'",
    ):
        Ipv6AddressValueObject(value='not-an-ipv6-address')


@mark.unit_testing
def test_ipv6_address_value_object_raises_invalid_ipv6_address() -> None:
    """
    Test Ipv6AddressValueObject defensive invalid-address error branch.
    """
    address: Any = Ipv6AddressValueObject(value='::1')

    with assert_raises(
        expected_exception=ValueError,
        match=r'Ipv6AddressValueObject value <<<not-an-ipv6-address>>> is not a valid IPv6 address.',
    ):
        address._raise_value_is_not_valid_ipv6_address(value='not-an-ipv6-address')


@mark.unit_testing
def test_ipv6_address_value_object_rejects_invalid_normalized_value(monkeypatch: MonkeyPatch) -> None:
    """
    Test Ipv6AddressValueObject defensive validation branch for invalid normalized values.
    """
    address: Any = Ipv6AddressValueObject(value='::1')

    monkeypatch.setattr(
        Ipv6AddressValueObject, '_ensure_value_is_normalized', lambda self, value: 'not-an-ipv6-address'
    )

    with assert_raises(
        expected_exception=ValueError,
        match=r'Ipv6AddressValueObject value <<<invalid-ipv6>>> is not a valid IPv6 address.',
    ):
        address._ensure_value_is_valid_ipv6_address(value='invalid-ipv6')
