"""
Test helpers for Spanish vehicle plate value objects.
"""

from typing import Any

from pytest import raises as assert_raises

from value_object_pattern.usables.identifiers.world.europe.spain import VehiclePlateValueObject


def assert_vehicle_plate_value_object_happy_path(
    *,
    value_object_type: Any,
    raw_value: str,
    expected_value: str,
) -> None:
    """
    Assert a vehicle plate value object happy path.
    """
    plate = value_object_type(value=raw_value)

    assert type(plate.value) is str
    assert plate.value == expected_value
    assert value_object_type.identification_regex().fullmatch(raw_value)
    assert value_object_type.validation_regex().fullmatch(expected_value)
    assert VehiclePlateValueObject(value=raw_value).value == expected_value


def assert_vehicle_plate_value_object_invalid_value(*, value_object_type: Any) -> None:
    """
    Assert a vehicle plate value object rejects invalid values.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'.*ValueObject value <<<invalid>>> is not a valid Spanish .*\.',
    ):
        value_object_type(value='invalid')


def assert_vehicle_plate_value_object_invalid_processed_value(
    *,
    value_object_type: Any,
    raw_value: str,
    expected_value: str,
) -> None:
    """
    Assert a vehicle plate value object rejects invalid processed values.
    """
    plate = value_object_type(value=raw_value)

    with assert_raises(
        expected_exception=ValueError,
        match=rf'.*ValueObject value <<<{expected_value}>>> is not a valid Spanish .*\.',
    ):
        plate._ensure_value_follows_validation_regex(value=expected_value, processed_value='INVALID')
