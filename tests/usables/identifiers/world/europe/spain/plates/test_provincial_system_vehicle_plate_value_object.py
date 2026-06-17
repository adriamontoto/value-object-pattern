"""
Test ProvincialSystemVehiclePlateValueObject value object.
"""

from pytest import mark, raises as assert_raises

from tests.usables.identifiers.world.europe.spain.plates.helpers import (
    assert_vehicle_plate_value_object_happy_path,
    assert_vehicle_plate_value_object_invalid_processed_value,
    assert_vehicle_plate_value_object_invalid_value,
)
from value_object_pattern.usables.identifiers.world.europe.spain.plates import ProvincialSystemVehiclePlateValueObject


@mark.unit_testing
def test_provincial_system_vehicle_plate_value_object_happy_path() -> None:
    """
    Test ProvincialSystemVehiclePlateValueObject value object happy path.
    """
    assert_vehicle_plate_value_object_happy_path(
        value_object_type=ProvincialSystemVehiclePlateValueObject,
        raw_value='m-1234-aa',
        expected_value='M1234AA',
    )


@mark.unit_testing
def test_provincial_system_vehicle_plate_value_object_invalid_value() -> None:
    """
    Test ProvincialSystemVehiclePlateValueObject value object raises ValueError for invalid values.
    """
    assert_vehicle_plate_value_object_invalid_value(value_object_type=ProvincialSystemVehiclePlateValueObject)


@mark.unit_testing
def test_provincial_system_vehicle_plate_value_object_invalid_processed_value() -> None:
    """
    Test ProvincialSystemVehiclePlateValueObject defensive validation branch for invalid processed values.
    """
    assert_vehicle_plate_value_object_invalid_processed_value(
        value_object_type=ProvincialSystemVehiclePlateValueObject,
        raw_value='m-1234-aa',
        expected_value='M1234AA',
    )


@mark.unit_testing
def test_provincial_system_vehicle_plate_value_object_unknown_provincial_code() -> None:
    """
    Test ProvincialSystemVehiclePlateValueObject value object rejects unknown provincial codes.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'ProvincialSystemVehiclePlateValueObject value <<<XX-1234-AA>>> is not a valid Spanish provincial system plate.',  # noqa: E501
    ):
        ProvincialSystemVehiclePlateValueObject(value='XX-1234-AA')
