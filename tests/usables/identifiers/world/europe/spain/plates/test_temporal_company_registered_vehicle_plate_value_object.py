"""
Test TemporalCompanyRegisteredVehiclePlateValueObject value object.
"""

from pytest import mark

from tests.usables.identifiers.world.europe.spain.plates.helpers import (
    assert_vehicle_plate_value_object_happy_path,
    assert_vehicle_plate_value_object_invalid_processed_value,
    assert_vehicle_plate_value_object_invalid_value,
)
from value_object_pattern.usables.identifiers.world.europe.spain.plates import (
    TemporalCompanyRegisteredVehiclePlateValueObject,
)


@mark.unit_testing
def test_temporal_company_registered_vehicle_plate_value_object_happy_path() -> None:
    """
    Test TemporalCompanyRegisteredVehiclePlateValueObject value object happy path.
    """
    assert_vehicle_plate_value_object_happy_path(
        value_object_type=TemporalCompanyRegisteredVehiclePlateValueObject,
        raw_value='v-1234-bcd',
        expected_value='V1234BCD',
    )


@mark.unit_testing
def test_temporal_company_registered_vehicle_plate_value_object_invalid_value() -> None:
    """
    Test TemporalCompanyRegisteredVehiclePlateValueObject value object raises ValueError for invalid values.
    """
    assert_vehicle_plate_value_object_invalid_value(value_object_type=TemporalCompanyRegisteredVehiclePlateValueObject)


@mark.unit_testing
def test_temporal_company_registered_vehicle_plate_value_object_invalid_processed_value() -> None:
    """
    Test TemporalCompanyRegisteredVehiclePlateValueObject defensive validation branch for invalid processed values.
    """
    assert_vehicle_plate_value_object_invalid_processed_value(
        value_object_type=TemporalCompanyRegisteredVehiclePlateValueObject,
        raw_value='v-1234-bcd',
        expected_value='V1234BCD',
    )
