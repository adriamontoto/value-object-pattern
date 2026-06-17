"""
Test helpers for MAC address value objects.
"""

from typing import Any

from pytest import raises as assert_raises


def assert_mac_address_value_object_happy_path(
    *,
    value_object_type: Any,
    raw_value: str,
    expected_value: str,
) -> None:
    """
    Assert a MAC address value object happy path.
    """
    mac_address = value_object_type(value=raw_value)

    assert type(mac_address.value) is str
    assert mac_address.value == expected_value
    assert value_object_type.identification_regex().fullmatch(raw_value)
    assert value_object_type.validation_regex().fullmatch(expected_value)


def assert_mac_address_value_object_invalid_value(*, value_object_type: Any) -> None:
    """
    Assert a MAC address value object rejects invalid values.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=rf'{value_object_type.__name__} value <<<invalid>>> is not .*',
    ):
        value_object_type(value='invalid')


def assert_mac_address_value_object_invalid_processed_value(
    *,
    value_object_type: Any,
    raw_value: str,
    expected_value: str,
) -> None:
    """
    Assert a MAC address value object rejects invalid processed values.
    """
    mac_address = value_object_type(value=raw_value)

    with assert_raises(
        expected_exception=ValueError,
        match=rf'{value_object_type.__name__} value <<<{expected_value}>>> is not .*',
    ):
        mac_address._ensure_value_follows_validation_regex(value=expected_value, processed_value='INVALID')
