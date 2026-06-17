"""
Test CanariasPoliceVehiclePlateValueObject value object.
"""

from pytest import mark

from tests.usables.identifiers.world.europe.spain.plates.helpers import (
    assert_vehicle_plate_value_object_happy_path,
    assert_vehicle_plate_value_object_invalid_processed_value,
    assert_vehicle_plate_value_object_invalid_value,
)
from value_object_pattern.usables.identifiers.world.europe.spain.plates import (
    CanariasPoliceVehiclePlateValueObject,
)


@mark.unit_testing
def test_canarias_police_vehicle_plate_value_object_happy_path() -> None:
    """
    Test CanariasPoliceVehiclePlateValueObject value object happy path.
    """
    assert_vehicle_plate_value_object_happy_path(
        value_object_type=CanariasPoliceVehiclePlateValueObject,
        raw_value='cgpc-1234',
        expected_value='CGPC1234',
    )


@mark.unit_testing
def test_canarias_police_vehicle_plate_value_object_invalid_value() -> None:
    """
    Test CanariasPoliceVehiclePlateValueObject value object raises ValueError for invalid values.
    """
    assert_vehicle_plate_value_object_invalid_value(value_object_type=CanariasPoliceVehiclePlateValueObject)


@mark.unit_testing
def test_canarias_police_vehicle_plate_value_object_invalid_processed_value() -> None:
    """
    Test CanariasPoliceVehiclePlateValueObject defensive validation branch for invalid processed values.
    """
    assert_vehicle_plate_value_object_invalid_processed_value(
        value_object_type=CanariasPoliceVehiclePlateValueObject,
        raw_value='cgpc-1234',
        expected_value='CGPC1234',
    )
