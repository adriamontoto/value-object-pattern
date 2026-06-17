"""
Test Spanish vehicle plate utility functions.
"""

from pytest import mark

from value_object_pattern.usables.identifiers.world.europe.spain.plates import utils as plate_utils


@mark.unit_testing
def test_plate_utils_load_provincial_plate_codes() -> None:
    """
    Test Spanish vehicle plate utility functions load provincial plate codes.
    """
    plate_utils.get_provincial_plate_codes.cache_clear()

    assert 'M' in plate_utils.get_provincial_plate_codes()
