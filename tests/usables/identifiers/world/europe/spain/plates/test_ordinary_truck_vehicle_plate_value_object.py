"""
Test OrdinaryTruckVehiclePlateValueObject value object.
"""

from pytest import mark

from tests.usables.identifiers.world.europe.spain.plates.helpers import (
    assert_vehicle_plate_value_object_happy_path,
    assert_vehicle_plate_value_object_invalid_processed_value,
    assert_vehicle_plate_value_object_invalid_value,
)
from value_object_pattern.usables.identifiers.world.europe.spain.plates import OrdinaryTruckVehiclePlateValueObject


@mark.unit_testing
def test_ordinary_truck_vehicle_plate_value_object_happy_path() -> None:
    """
    Test OrdinaryTruckVehiclePlateValueObject value object happy path.
    """
    assert_vehicle_plate_value_object_happy_path(
        value_object_type=OrdinaryTruckVehiclePlateValueObject,
        raw_value='r-1234-bcd',
        expected_value='R1234BCD',
    )


@mark.unit_testing
def test_ordinary_truck_vehicle_plate_value_object_invalid_value() -> None:
    """
    Test OrdinaryTruckVehiclePlateValueObject value object raises ValueError for invalid values.
    """
    assert_vehicle_plate_value_object_invalid_value(value_object_type=OrdinaryTruckVehiclePlateValueObject)


@mark.unit_testing
def test_ordinary_truck_vehicle_plate_value_object_invalid_processed_value() -> None:
    """
    Test OrdinaryTruckVehiclePlateValueObject defensive validation branch for invalid processed values.
    """
    assert_vehicle_plate_value_object_invalid_processed_value(
        value_object_type=OrdinaryTruckVehiclePlateValueObject,
        raw_value='r-1234-bcd',
        expected_value='R1234BCD',
    )
