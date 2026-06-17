"""
Test AirForceVehiclePlateValueObject value object.
"""

from pytest import mark

from tests.usables.identifiers.world.europe.spain.plates.helpers import (
    assert_vehicle_plate_value_object_happy_path,
    assert_vehicle_plate_value_object_invalid_processed_value,
    assert_vehicle_plate_value_object_invalid_value,
)
from value_object_pattern.usables.identifiers.world.europe.spain.plates import AirForceVehiclePlateValueObject


@mark.unit_testing
def test_air_force_vehicle_plate_value_object_happy_path() -> None:
    """
    Test AirForceVehiclePlateValueObject value object happy path.
    """
    assert_vehicle_plate_value_object_happy_path(
        value_object_type=AirForceVehiclePlateValueObject,
        raw_value='ea12343',
        expected_value='EA12343',
    )


@mark.unit_testing
def test_air_force_vehicle_plate_value_object_invalid_value() -> None:
    """
    Test AirForceVehiclePlateValueObject value object raises ValueError for invalid values.
    """
    assert_vehicle_plate_value_object_invalid_value(value_object_type=AirForceVehiclePlateValueObject)


@mark.unit_testing
def test_air_force_vehicle_plate_value_object_invalid_processed_value() -> None:
    """
    Test AirForceVehiclePlateValueObject defensive validation branch for invalid processed values.
    """
    assert_vehicle_plate_value_object_invalid_processed_value(
        value_object_type=AirForceVehiclePlateValueObject,
        raw_value='ea12343',
        expected_value='EA12343',
    )
