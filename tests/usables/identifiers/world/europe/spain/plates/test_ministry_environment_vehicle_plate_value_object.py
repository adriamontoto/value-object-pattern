"""
Test MinistryEnvironmentVehiclePlateValueObject value object.
"""

from pytest import mark

from tests.usables.identifiers.world.europe.spain.plates.helpers import (
    assert_vehicle_plate_value_object_happy_path,
    assert_vehicle_plate_value_object_invalid_processed_value,
    assert_vehicle_plate_value_object_invalid_value,
)
from value_object_pattern.usables.identifiers.world.europe.spain.plates import (
    MinistryEnvironmentVehiclePlateValueObject,
)


@mark.unit_testing
def test_ministry_environment_vehicle_plate_value_object_happy_path() -> None:
    """
    Test MinistryEnvironmentVehiclePlateValueObject value object happy path.
    """
    assert_vehicle_plate_value_object_happy_path(
        value_object_type=MinistryEnvironmentVehiclePlateValueObject,
        raw_value='mf-12345-a',
        expected_value='MF12345A',
    )


@mark.unit_testing
def test_ministry_environment_vehicle_plate_value_object_invalid_value() -> None:
    """
    Test MinistryEnvironmentVehiclePlateValueObject value object raises ValueError for invalid values.
    """
    assert_vehicle_plate_value_object_invalid_value(value_object_type=MinistryEnvironmentVehiclePlateValueObject)


@mark.unit_testing
def test_ministry_environment_vehicle_plate_value_object_invalid_processed_value() -> None:
    """
    Test MinistryEnvironmentVehiclePlateValueObject defensive validation branch for invalid processed values.
    """
    assert_vehicle_plate_value_object_invalid_processed_value(
        value_object_type=MinistryEnvironmentVehiclePlateValueObject,
        raw_value='mf-12345-a',
        expected_value='MF12345A',
    )
