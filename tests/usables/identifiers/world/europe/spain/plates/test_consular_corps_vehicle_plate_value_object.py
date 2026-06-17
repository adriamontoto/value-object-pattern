"""
Test ConsularCorpsVehiclePlateValueObject value object.
"""

from pytest import mark

from tests.usables.identifiers.world.europe.spain.plates.helpers import (
    assert_vehicle_plate_value_object_happy_path,
    assert_vehicle_plate_value_object_invalid_processed_value,
    assert_vehicle_plate_value_object_invalid_value,
)
from value_object_pattern.usables.identifiers.world.europe.spain.plates import ConsularCorpsVehiclePlateValueObject


@mark.unit_testing
def test_consular_corps_vehicle_plate_value_object_happy_path() -> None:
    """
    Test ConsularCorpsVehiclePlateValueObject value object happy path.
    """
    assert_vehicle_plate_value_object_happy_path(
        value_object_type=ConsularCorpsVehiclePlateValueObject,
        raw_value='cc-1-234',
        expected_value='CC1234',
    )


@mark.unit_testing
def test_consular_corps_vehicle_plate_value_object_invalid_value() -> None:
    """
    Test ConsularCorpsVehiclePlateValueObject value object raises ValueError for invalid values.
    """
    assert_vehicle_plate_value_object_invalid_value(value_object_type=ConsularCorpsVehiclePlateValueObject)


@mark.unit_testing
def test_consular_corps_vehicle_plate_value_object_invalid_processed_value() -> None:
    """
    Test ConsularCorpsVehiclePlateValueObject defensive validation branch for invalid processed values.
    """
    assert_vehicle_plate_value_object_invalid_processed_value(
        value_object_type=ConsularCorpsVehiclePlateValueObject,
        raw_value='cc-1-234',
        expected_value='CC1234',
    )
