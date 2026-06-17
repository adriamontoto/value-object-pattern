"""
Test VehiclePlateValueObject value object.
"""

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.identifiers.world.europe.spain import VehiclePlateValueObject


@mark.unit_testing
def test_vehicle_plate_value_object_happy_path() -> None:
    """
    Test VehiclePlateValueObject value object happy path.
    """
    plate = VehiclePlateValueObject(value='1234-bcd')

    assert type(plate.value) is str
    assert plate.value == '1234BCD'


@mark.unit_testing
def test_vehicle_plate_value_object_invalid_value() -> None:
    """
    Test VehiclePlateValueObject value object raises ValueError when value is not a Spanish vehicle plate.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'VehiclePlateValueObject value <<<invalid-plate>>> is not a valid Spanish vehicle plate.',
    ):
        VehiclePlateValueObject(value='invalid-plate')


@mark.unit_testing
def test_vehicle_plate_value_object_formatting_returns_none_for_unknown_plate() -> None:
    """
    Test VehiclePlateValueObject defensive formatting branch for unknown plate variations.
    """
    plate = VehiclePlateValueObject(value='1234-bcd')

    assert plate._ensure_value_is_formatted(value='invalid-plate') is None
