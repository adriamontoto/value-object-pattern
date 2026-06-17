"""
Test ArmyVehiclePlateValueObject value object.
"""

from pytest import mark

from tests.usables.identifiers.world.europe.spain.plates.helpers import (
    assert_vehicle_plate_value_object_happy_path,
    assert_vehicle_plate_value_object_invalid_processed_value,
    assert_vehicle_plate_value_object_invalid_value,
)
from value_object_pattern.usables.identifiers.world.europe.spain.plates import ArmyVehiclePlateValueObject


@mark.unit_testing
def test_army_vehicle_plate_value_object_happy_path() -> None:
    """
    Test ArmyVehiclePlateValueObject value object happy path.
    """
    assert_vehicle_plate_value_object_happy_path(
        value_object_type=ArmyVehiclePlateValueObject,
        raw_value='et-12345',
        expected_value='ET12345',
    )


@mark.unit_testing
def test_army_vehicle_plate_value_object_invalid_value() -> None:
    """
    Test ArmyVehiclePlateValueObject value object raises ValueError for invalid values.
    """
    assert_vehicle_plate_value_object_invalid_value(value_object_type=ArmyVehiclePlateValueObject)


@mark.unit_testing
def test_army_vehicle_plate_value_object_invalid_processed_value() -> None:
    """
    Test ArmyVehiclePlateValueObject defensive validation branch for invalid processed values.
    """
    assert_vehicle_plate_value_object_invalid_processed_value(
        value_object_type=ArmyVehiclePlateValueObject,
        raw_value='et-12345',
        expected_value='ET12345',
    )
