"""
Test Spanish identifier utility functions.
"""

from pytest import mark

from value_object_pattern.usables.identifiers.world.europe.spain import utils as spain_utils


@mark.unit_testing
def test_spain_utils_load_provincial_codes() -> None:
    """
    Test Spanish identifier utility functions load provincial codes.
    """
    spain_utils.get_provincial_codes.cache_clear()

    assert 28 in spain_utils.get_provincial_codes()
