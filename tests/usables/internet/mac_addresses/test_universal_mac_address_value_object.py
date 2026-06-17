"""
Test UniversalMacAddressValueObject value object.
"""

from pytest import mark

from tests.usables.internet.mac_addresses.helpers import (
    assert_mac_address_value_object_happy_path,
    assert_mac_address_value_object_invalid_processed_value,
    assert_mac_address_value_object_invalid_value,
)
from value_object_pattern.usables.internet.mac_addresses import UniversalMacAddressValueObject


@mark.unit_testing
def test_universal_mac_address_value_object_happy_path() -> None:
    """
    Test UniversalMacAddressValueObject value object happy path.
    """
    assert_mac_address_value_object_happy_path(
        value_object_type=UniversalMacAddressValueObject,
        raw_value='d5:b9:eb:4d:c2:cc',
        expected_value='D5:B9:EB:4D:C2:CC',
    )


@mark.unit_testing
def test_universal_mac_address_value_object_conversions() -> None:
    """
    Test UniversalMacAddressValueObject value object conversions.
    """
    mac_address = UniversalMacAddressValueObject(value='d5:b9:eb:4d:c2:cc')

    assert mac_address.to_raw().value == 'D5B9EB4DC2CC'
    assert mac_address.to_windows().value == 'D5-B9-EB-4D-C2-CC'
    assert mac_address.to_cisco().value == 'D5B9.EB4D.C2CC'
    assert mac_address.to_space().value == 'D5 B9 EB 4D C2 CC'


@mark.unit_testing
def test_universal_mac_address_value_object_invalid_value() -> None:
    """
    Test UniversalMacAddressValueObject value object raises ValueError for invalid values.
    """
    assert_mac_address_value_object_invalid_value(value_object_type=UniversalMacAddressValueObject)


@mark.unit_testing
def test_universal_mac_address_value_object_invalid_processed_value() -> None:
    """
    Test UniversalMacAddressValueObject defensive validation branch for invalid processed values.
    """
    assert_mac_address_value_object_invalid_processed_value(
        value_object_type=UniversalMacAddressValueObject,
        raw_value='d5:b9:eb:4d:c2:cc',
        expected_value='D5:B9:EB:4D:C2:CC',
    )
