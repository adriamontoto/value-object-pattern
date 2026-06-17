"""
Test MacAddressValueObject value object.
"""

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.internet import MacAddressValueObject


@mark.unit_testing
def test_mac_address_value_object_accepts_raw_format() -> None:
    """
    Test MacAddressValueObject value object accepts raw MAC addresses.
    """
    assert MacAddressValueObject(value='d5b9eb4dc2cc').value == 'D5B9EB4DC2CC'


@mark.unit_testing
def test_mac_address_value_object_accepts_universal_format() -> None:
    """
    Test MacAddressValueObject value object accepts universal MAC addresses.
    """
    assert MacAddressValueObject(value='d5:b9:eb:4d:c2:cc').value == 'D5B9EB4DC2CC'


@mark.unit_testing
def test_mac_address_value_object_accepts_windows_format() -> None:
    """
    Test MacAddressValueObject value object accepts Windows MAC addresses.
    """
    assert MacAddressValueObject(value='d5-b9-eb-4d-c2-cc').value == 'D5B9EB4DC2CC'


@mark.unit_testing
def test_mac_address_value_object_accepts_cisco_format() -> None:
    """
    Test MacAddressValueObject value object accepts Cisco MAC addresses.
    """
    assert MacAddressValueObject(value='d5b9.eb4d.c2cc').value == 'D5B9EB4DC2CC'


@mark.unit_testing
def test_mac_address_value_object_accepts_space_format() -> None:
    """
    Test MacAddressValueObject value object accepts space-separated MAC addresses.
    """
    assert MacAddressValueObject(value='d5 b9 eb 4d c2 cc').value == 'D5B9EB4DC2CC'


@mark.unit_testing
def test_mac_address_value_object_conversions() -> None:
    """
    Test MacAddressValueObject value object conversions.
    """
    mac_address = MacAddressValueObject(value='d5:b9:eb:4d:c2:cc')

    assert mac_address.to_raw().value == 'D5B9EB4DC2CC'
    assert mac_address.to_universal().value == 'D5:B9:EB:4D:C2:CC'
    assert mac_address.to_windows().value == 'D5-B9-EB-4D-C2-CC'
    assert mac_address.to_cisco().value == 'D5B9.EB4D.C2CC'
    assert mac_address.to_space().value == 'D5 B9 EB 4D C2 CC'


@mark.unit_testing
def test_mac_address_value_object_classmethods() -> None:
    """
    Test MacAddressValueObject class constructors.
    """
    assert MacAddressValueObject.NULL().value == '000000000000'
    assert MacAddressValueObject.BROADCAST().value == 'FFFFFFFFFFFF'


@mark.unit_testing
def test_mac_address_value_object_invalid_value() -> None:
    """
    Test MacAddressValueObject value object raises ValueError when value is not a MAC address.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'MacAddressValueObject value <<<invalid>>> is not a valid MAC address.',
    ):
        MacAddressValueObject(value='invalid')


@mark.unit_testing
def test_mac_address_value_object_formatting_returns_none_for_unknown_mac_address() -> None:
    """
    Test MacAddressValueObject defensive formatting branch for unknown MAC address variations.
    """
    mac_address = MacAddressValueObject(value='d5:b9:eb:4d:c2:cc')

    assert mac_address._ensure_value_is_formatted(value='invalid') is None
