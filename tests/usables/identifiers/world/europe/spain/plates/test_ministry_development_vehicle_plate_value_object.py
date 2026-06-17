"""
Test MinistryDevelopmentVehiclePlateValueObject value object.
"""

from pytest import mark

from tests.usables.identifiers.world.europe.spain.plates.helpers import (
    assert_vehicle_plate_value_object_happy_path,
    assert_vehicle_plate_value_object_invalid_processed_value,
    assert_vehicle_plate_value_object_invalid_value,
)
from value_object_pattern.usables.identifiers.world.europe.spain.plates import (
    MinistryDevelopmentVehiclePlateValueObject,
)


@mark.unit_testing
def test_ministry_development_vehicle_plate_value_object_happy_path() -> None:
    """
    Test MinistryDevelopmentVehiclePlateValueObject value object happy path.
    """
    assert_vehicle_plate_value_object_happy_path(
        value_object_type=MinistryDevelopmentVehiclePlateValueObject,
        raw_value='mma-12345-a',
        expected_value='MMA12345A',
    )


@mark.unit_testing
def test_ministry_development_vehicle_plate_value_object_invalid_value() -> None:
    """
    Test MinistryDevelopmentVehiclePlateValueObject value object raises ValueError for invalid values.
    """
    assert_vehicle_plate_value_object_invalid_value(value_object_type=MinistryDevelopmentVehiclePlateValueObject)


@mark.unit_testing
def test_ministry_development_vehicle_plate_value_object_invalid_processed_value() -> None:
    """
    Test MinistryDevelopmentVehiclePlateValueObject defensive validation branch for invalid processed values.
    """
    assert_vehicle_plate_value_object_invalid_processed_value(
        value_object_type=MinistryDevelopmentVehiclePlateValueObject,
        raw_value='mma-12345-a',
        expected_value='MMA12345A',
    )
