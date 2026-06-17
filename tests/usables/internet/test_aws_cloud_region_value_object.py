"""
Test AwsCloudRegionValueObject value object.
"""

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.internet import AwsCloudRegionValueObject


@mark.unit_testing
def test_aws_cloud_region_value_object_happy_path() -> None:
    """
    Test AwsCloudRegionValueObject value object happy path.
    """
    region = AwsCloudRegionValueObject(value='US-EAST-1')

    assert type(region.value) is str
    assert region.value == 'us-east-1'


@mark.unit_testing
def test_aws_cloud_region_value_object_invalid_value() -> None:
    """
    Test AwsCloudRegionValueObject value object raises ValueError when value is not a valid AWS cloud region.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'AwsCloudRegionValueObject value <<<moon-west-1>>> is not a valid AWS cloud region.',
    ):
        AwsCloudRegionValueObject(value='moon-west-1')
