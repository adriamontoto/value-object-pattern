"""
Test RawMacAddressValueObject value object.
"""

from pytest import mark

from tests.usables.internet.mac_addresses.helpers import (
    assert_mac_address_value_object_happy_path,
    assert_mac_address_value_object_invalid_processed_value,
    assert_mac_address_value_object_invalid_value,
)
from value_object_pattern.usables.internet.mac_addresses import RawMacAddressValueObject


@mark.unit_testing
def test_raw_mac_address_value_object_happy_path() -> None:
    """
    Test RawMacAddressValueObject value object happy path.
    """
    assert_mac_address_value_object_happy_path(
        value_object_type=RawMacAddressValueObject,
        raw_value='d5b9eb4dc2cc',
        expected_value='D5B9EB4DC2CC',
    )


@mark.unit_testing
def test_raw_mac_address_value_object_conversions() -> None:
    """
    Test RawMacAddressValueObject value object conversions.
    """
    mac_address = RawMacAddressValueObject(value='d5b9eb4dc2cc')

    assert mac_address.to_universal().value == 'D5:B9:EB:4D:C2:CC'
    assert mac_address.to_windows().value == 'D5-B9-EB-4D-C2-CC'
    assert mac_address.to_cisco().value == 'D5B9.EB4D.C2CC'
    assert mac_address.to_space().value == 'D5 B9 EB 4D C2 CC'


@mark.unit_testing
def test_raw_mac_address_value_object_invalid_value() -> None:
    """
    Test RawMacAddressValueObject value object raises ValueError for invalid values.
    """
    assert_mac_address_value_object_invalid_value(value_object_type=RawMacAddressValueObject)


@mark.unit_testing
def test_raw_mac_address_value_object_invalid_processed_value() -> None:
    """
    Test RawMacAddressValueObject defensive validation branch for invalid processed values.
    """
    assert_mac_address_value_object_invalid_processed_value(
        value_object_type=RawMacAddressValueObject,
        raw_value='d5b9eb4dc2cc',
        expected_value='D5B9EB4DC2CC',
    )
