"""
Test NationalPoliceVehiclePlateValueObject value object.
"""

from pytest import mark

from tests.usables.identifiers.world.europe.spain.plates.helpers import (
    assert_vehicle_plate_value_object_happy_path,
    assert_vehicle_plate_value_object_invalid_processed_value,
    assert_vehicle_plate_value_object_invalid_value,
)
from value_object_pattern.usables.identifiers.world.europe.spain.plates import NationalPoliceVehiclePlateValueObject


@mark.unit_testing
def test_national_police_vehicle_plate_value_object_happy_path() -> None:
    """
    Test NationalPoliceVehiclePlateValueObject value object happy path.
    """
    assert_vehicle_plate_value_object_happy_path(
        value_object_type=NationalPoliceVehiclePlateValueObject,
        raw_value='cnp-1234-ab',
        expected_value='CNP1234AB',
    )


@mark.unit_testing
def test_national_police_vehicle_plate_value_object_invalid_value() -> None:
    """
    Test NationalPoliceVehiclePlateValueObject value object raises ValueError for invalid values.
    """
    assert_vehicle_plate_value_object_invalid_value(value_object_type=NationalPoliceVehiclePlateValueObject)


@mark.unit_testing
def test_national_police_vehicle_plate_value_object_invalid_processed_value() -> None:
    """
    Test NationalPoliceVehiclePlateValueObject defensive validation branch for invalid processed values.
    """
    assert_vehicle_plate_value_object_invalid_processed_value(
        value_object_type=NationalPoliceVehiclePlateValueObject,
        raw_value='cnp-1234-ab',
        expected_value='CNP1234AB',
    )
