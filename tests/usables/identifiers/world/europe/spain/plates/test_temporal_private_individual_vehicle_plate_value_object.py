"""
Test TemporalPrivateIndividualVehiclePlateValueObject value object.
"""

from pytest import mark

from tests.usables.identifiers.world.europe.spain.plates.helpers import (
    assert_vehicle_plate_value_object_happy_path,
    assert_vehicle_plate_value_object_invalid_processed_value,
    assert_vehicle_plate_value_object_invalid_value,
)
from value_object_pattern.usables.identifiers.world.europe.spain.plates import (
    TemporalPrivateIndividualVehiclePlateValueObject,
)


@mark.unit_testing
def test_temporal_private_individual_vehicle_plate_value_object_happy_path() -> None:
    """
    Test TemporalPrivateIndividualVehiclePlateValueObject value object happy path.
    """
    assert_vehicle_plate_value_object_happy_path(
        value_object_type=TemporalPrivateIndividualVehiclePlateValueObject,
        raw_value='t-1234-bcd',
        expected_value='T1234BCD',
    )


@mark.unit_testing
def test_temporal_private_individual_vehicle_plate_value_object_invalid_value() -> None:
    """
    Test TemporalPrivateIndividualVehiclePlateValueObject value object raises ValueError for invalid values.
    """
    assert_vehicle_plate_value_object_invalid_value(
        value_object_type=TemporalPrivateIndividualVehiclePlateValueObject,
    )


@mark.unit_testing
def test_temporal_private_individual_vehicle_plate_value_object_invalid_processed_value() -> None:
    """
    Test TemporalPrivateIndividualVehiclePlateValueObject defensive validation branch for invalid processed values.
    """
    assert_vehicle_plate_value_object_invalid_processed_value(
        value_object_type=TemporalPrivateIndividualVehiclePlateValueObject,
        raw_value='t-1234-bcd',
        expected_value='T1234BCD',
    )
