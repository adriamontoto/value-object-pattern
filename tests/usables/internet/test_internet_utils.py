"""
Test internet utility functions.
"""

from pytest import mark

from value_object_pattern.usables.internet import utils as internet_utils


@mark.unit_testing
def test_internet_utils_load_aws_cloud_regions() -> None:
    """
    Test internet utility functions load AWS cloud regions.
    """
    internet_utils.get_aws_cloud_regions.cache_clear()

    assert 'us-east-1' in internet_utils.get_aws_cloud_regions()


@mark.unit_testing
def test_internet_utils_load_tlds() -> None:
    """
    Test internet utility functions load top-level domains.
    """
    internet_utils.get_tld_dict.cache_clear()

    assert 'com' in internet_utils.get_tld_dict()
