"""
Test AdministrativeTechnicianVehiclePlateValueObject value object.
"""

from pytest import mark

from tests.usables.identifiers.world.europe.spain.plates.helpers import (
    assert_vehicle_plate_value_object_happy_path,
    assert_vehicle_plate_value_object_invalid_processed_value,
    assert_vehicle_plate_value_object_invalid_value,
)
from value_object_pattern.usables.identifiers.world.europe.spain.plates import (
    AdministrativeTechnicianVehiclePlateValueObject,
)


@mark.unit_testing
def test_administrative_technician_vehicle_plate_value_object_happy_path() -> None:
    """
    Test AdministrativeTechnicianVehiclePlateValueObject value object happy path.
    """
    assert_vehicle_plate_value_object_happy_path(
        value_object_type=AdministrativeTechnicianVehiclePlateValueObject,
        raw_value='ta-1-234',
        expected_value='TA1234',
    )


@mark.unit_testing
def test_administrative_technician_vehicle_plate_value_object_invalid_value() -> None:
    """
    Test AdministrativeTechnicianVehiclePlateValueObject value object raises ValueError for invalid values.
    """
    assert_vehicle_plate_value_object_invalid_value(value_object_type=AdministrativeTechnicianVehiclePlateValueObject)


@mark.unit_testing
def test_administrative_technician_vehicle_plate_value_object_invalid_processed_value() -> None:
    """
    Test AdministrativeTechnicianVehiclePlateValueObject defensive validation branch for invalid processed values.
    """
    assert_vehicle_plate_value_object_invalid_processed_value(
        value_object_type=AdministrativeTechnicianVehiclePlateValueObject,
        raw_value='ta-1-234',
        expected_value='TA1234',
    )
