"""
Test OrdinaryVehiclePlateValueObject value object.
"""

from pytest import mark

from tests.usables.identifiers.world.europe.spain.plates.helpers import (
    assert_vehicle_plate_value_object_happy_path,
    assert_vehicle_plate_value_object_invalid_processed_value,
    assert_vehicle_plate_value_object_invalid_value,
)
from value_object_pattern.usables.identifiers.world.europe.spain.plates import OrdinaryVehiclePlateValueObject


@mark.unit_testing
def test_ordinary_vehicle_plate_value_object_happy_path() -> None:
    """
    Test OrdinaryVehiclePlateValueObject value object happy path.
    """
    assert_vehicle_plate_value_object_happy_path(
        value_object_type=OrdinaryVehiclePlateValueObject,
        raw_value='1234-bcd',
        expected_value='1234BCD',
    )


@mark.unit_testing
def test_ordinary_vehicle_plate_value_object_invalid_value() -> None:
    """
    Test OrdinaryVehiclePlateValueObject value object raises ValueError for invalid values.
    """
    assert_vehicle_plate_value_object_invalid_value(value_object_type=OrdinaryVehiclePlateValueObject)


@mark.unit_testing
def test_ordinary_vehicle_plate_value_object_invalid_processed_value() -> None:
    """
    Test OrdinaryVehiclePlateValueObject defensive validation branch for invalid processed values.
    """
    assert_vehicle_plate_value_object_invalid_processed_value(
        value_object_type=OrdinaryVehiclePlateValueObject,
        raw_value='1234-bcd',
        expected_value='1234BCD',
    )
