"""
Test TemporalCompanyNotRegisteredVehiclePlateValueObject value object.
"""

from pytest import mark

from tests.usables.identifiers.world.europe.spain.plates.helpers import (
    assert_vehicle_plate_value_object_happy_path,
    assert_vehicle_plate_value_object_invalid_processed_value,
    assert_vehicle_plate_value_object_invalid_value,
)
from value_object_pattern.usables.identifiers.world.europe.spain.plates import (
    TemporalCompanyNotRegisteredVehiclePlateValueObject,
)


@mark.unit_testing
def test_temporal_company_not_registered_vehicle_plate_value_object_happy_path() -> None:
    """
    Test TemporalCompanyNotRegisteredVehiclePlateValueObject value object happy path.
    """
    assert_vehicle_plate_value_object_happy_path(
        value_object_type=TemporalCompanyNotRegisteredVehiclePlateValueObject,
        raw_value='s-1234-bcd',
        expected_value='S1234BCD',
    )


@mark.unit_testing
def test_temporal_company_not_registered_vehicle_plate_value_object_invalid_value() -> None:
    """
    Test TemporalCompanyNotRegisteredVehiclePlateValueObject value object raises ValueError for invalid values.
    """
    assert_vehicle_plate_value_object_invalid_value(
        value_object_type=TemporalCompanyNotRegisteredVehiclePlateValueObject,
    )


@mark.unit_testing
def test_temporal_company_not_registered_vehicle_plate_value_object_invalid_processed_value() -> None:
    """
    Test TemporalCompanyNotRegisteredVehiclePlateValueObject defensive validation branch for invalid processed values.
    """
    assert_vehicle_plate_value_object_invalid_processed_value(
        value_object_type=TemporalCompanyNotRegisteredVehiclePlateValueObject,
        raw_value='s-1234-bcd',
        expected_value='S1234BCD',
    )
