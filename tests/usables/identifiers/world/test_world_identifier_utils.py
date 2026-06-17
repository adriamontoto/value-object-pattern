"""
Test world identifier utility functions.
"""

from pytest import mark

from value_object_pattern.usables.identifiers.world import utils as world_utils


@mark.unit_testing
def test_world_identifier_utils_load_iso3166_alpha2_codes() -> None:
    """
    Test world identifier utility functions load ISO 3166 alpha-2 codes.
    """
    world_utils.get_iso3166_alpha2_codes.cache_clear()

    assert 'ES' in world_utils.get_iso3166_alpha2_codes()


@mark.unit_testing
def test_world_identifier_utils_load_iso3166_alpha2_to_alpha3_mapping() -> None:
    """
    Test world identifier utility functions load ISO 3166 alpha-2 to alpha-3 mapping.
    """
    world_utils.get_iso3166_alpha2_to_alpha3_mapping.cache_clear()

    assert world_utils.get_iso3166_alpha2_to_alpha3_mapping()[0]['ES'] == 'ESP'


@mark.unit_testing
def test_world_identifier_utils_load_iso3166_alpha2_to_numeric_mapping() -> None:
    """
    Test world identifier utility functions load ISO 3166 alpha-2 to numeric mapping.
    """
    world_utils.get_iso3166_alpha2_to_numeric_mapping.cache_clear()

    assert world_utils.get_iso3166_alpha2_to_numeric_mapping()[0]['ES'] == 724


@mark.unit_testing
def test_world_identifier_utils_load_iso3166_alpha2_to_phone_code_mapping() -> None:
    """
    Test world identifier utility functions load ISO 3166 alpha-2 to phone code mapping.
    """
    world_utils.get_iso3166_alpha2_to_phone_code_mapping.cache_clear()

    assert world_utils.get_iso3166_alpha2_to_phone_code_mapping()[0]['ES'] == '34'


@mark.unit_testing
def test_world_identifier_utils_load_iso3166_alpha2_to_tld_mapping() -> None:
    """
    Test world identifier utility functions load ISO 3166 alpha-2 to TLD mapping.
    """
    world_utils.get_iso3166_alpha2_to_tld_mapping.cache_clear()

    assert world_utils.get_iso3166_alpha2_to_tld_mapping()[0]['ES'] == 'es'


@mark.unit_testing
def test_world_identifier_utils_load_iso3166_alpha3_codes() -> None:
    """
    Test world identifier utility functions load ISO 3166 alpha-3 codes.
    """
    world_utils.get_iso3166_alpha3_codes.cache_clear()

    assert 'ESP' in world_utils.get_iso3166_alpha3_codes()


@mark.unit_testing
def test_world_identifier_utils_load_iso3166_numeric_codes() -> None:
    """
    Test world identifier utility functions load ISO 3166 numeric codes.
    """
    world_utils.get_iso3166_numeric_codes.cache_clear()

    assert 724 in world_utils.get_iso3166_numeric_codes()
