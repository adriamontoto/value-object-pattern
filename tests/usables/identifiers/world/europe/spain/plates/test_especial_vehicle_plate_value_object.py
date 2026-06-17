"""
Test EspecialVehiclePlateValueObject value object.
"""

from pytest import mark

from tests.usables.identifiers.world.europe.spain.plates.helpers import (
    assert_vehicle_plate_value_object_happy_path,
    assert_vehicle_plate_value_object_invalid_processed_value,
    assert_vehicle_plate_value_object_invalid_value,
)
from value_object_pattern.usables.identifiers.world.europe.spain.plates import EspecialVehiclePlateValueObject


@mark.unit_testing
def test_especial_vehicle_plate_value_object_happy_path() -> None:
    """
    Test EspecialVehiclePlateValueObject value object happy path.
    """
    assert_vehicle_plate_value_object_happy_path(
        value_object_type=EspecialVehiclePlateValueObject,
        raw_value='e-1234-abc',
        expected_value='E1234ABC',
    )


@mark.unit_testing
def test_especial_vehicle_plate_value_object_invalid_value() -> None:
    """
    Test EspecialVehiclePlateValueObject value object raises ValueError for invalid values.
    """
    assert_vehicle_plate_value_object_invalid_value(value_object_type=EspecialVehiclePlateValueObject)


@mark.unit_testing
def test_especial_vehicle_plate_value_object_invalid_processed_value() -> None:
    """
    Test EspecialVehiclePlateValueObject defensive validation branch for invalid processed values.
    """
    assert_vehicle_plate_value_object_invalid_processed_value(
        value_object_type=EspecialVehiclePlateValueObject,
        raw_value='e-1234-abc',
        expected_value='E1234ABC',
    )
