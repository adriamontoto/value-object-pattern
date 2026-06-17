"""
Test CiscoMacAddressValueObject value object.
"""

from pytest import mark

from tests.usables.internet.mac_addresses.helpers import (
    assert_mac_address_value_object_happy_path,
    assert_mac_address_value_object_invalid_processed_value,
    assert_mac_address_value_object_invalid_value,
)
from value_object_pattern.usables.internet.mac_addresses import CiscoMacAddressValueObject


@mark.unit_testing
def test_cisco_mac_address_value_object_happy_path() -> None:
    """
    Test CiscoMacAddressValueObject value object happy path.
    """
    assert_mac_address_value_object_happy_path(
        value_object_type=CiscoMacAddressValueObject,
        raw_value='d5b9.eb4d.c2cc',
        expected_value='D5B9.EB4D.C2CC',
    )


@mark.unit_testing
def test_cisco_mac_address_value_object_conversions() -> None:
    """
    Test CiscoMacAddressValueObject value object conversions.
    """
    mac_address = CiscoMacAddressValueObject(value='d5b9.eb4d.c2cc')

    assert mac_address.to_raw().value == 'D5B9EB4DC2CC'
    assert mac_address.to_universal().value == 'D5:B9:EB:4D:C2:CC'
    assert mac_address.to_windows().value == 'D5-B9-EB-4D-C2-CC'
    assert mac_address.to_space().value == 'D5 B9 EB 4D C2 CC'


@mark.unit_testing
def test_cisco_mac_address_value_object_invalid_value() -> None:
    """
    Test CiscoMacAddressValueObject value object raises ValueError for invalid values.
    """
    assert_mac_address_value_object_invalid_value(value_object_type=CiscoMacAddressValueObject)


@mark.unit_testing
def test_cisco_mac_address_value_object_invalid_processed_value() -> None:
    """
    Test CiscoMacAddressValueObject defensive validation branch for invalid processed values.
    """
    assert_mac_address_value_object_invalid_processed_value(
        value_object_type=CiscoMacAddressValueObject,
        raw_value='d5b9.eb4d.c2cc',
        expected_value='D5B9.EB4D.C2CC',
    )
