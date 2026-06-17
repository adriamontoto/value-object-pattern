"""
Test StateMotorPoolVehiclePlateValueObject value object.
"""

from pytest import mark

from tests.usables.identifiers.world.europe.spain.plates.helpers import (
    assert_vehicle_plate_value_object_happy_path,
    assert_vehicle_plate_value_object_invalid_processed_value,
    assert_vehicle_plate_value_object_invalid_value,
)
from value_object_pattern.usables.identifiers.world.europe.spain.plates import StateMotorPoolVehiclePlateValueObject


@mark.unit_testing
def test_state_motor_pool_vehicle_plate_value_object_happy_path() -> None:
    """
    Test StateMotorPoolVehiclePlateValueObject value object happy path.
    """
    assert_vehicle_plate_value_object_happy_path(
        value_object_type=StateMotorPoolVehiclePlateValueObject,
        raw_value='pme-1234-a',
        expected_value='PME1234A',
    )


@mark.unit_testing
def test_state_motor_pool_vehicle_plate_value_object_invalid_value() -> None:
    """
    Test StateMotorPoolVehiclePlateValueObject value object raises ValueError for invalid values.
    """
    assert_vehicle_plate_value_object_invalid_value(value_object_type=StateMotorPoolVehiclePlateValueObject)


@mark.unit_testing
def test_state_motor_pool_vehicle_plate_value_object_invalid_processed_value() -> None:
    """
    Test StateMotorPoolVehiclePlateValueObject defensive validation branch for invalid processed values.
    """
    assert_vehicle_plate_value_object_invalid_processed_value(
        value_object_type=StateMotorPoolVehiclePlateValueObject,
        raw_value='pme-1234-a',
        expected_value='PME1234A',
    )
