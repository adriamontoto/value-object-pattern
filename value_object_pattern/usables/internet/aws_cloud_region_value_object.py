"""
AwsCloudRegionValueObject value object.
"""

from functools import lru_cache
from re import DOTALL, findall
from urllib.request import urlopen

from value_object_pattern import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


@lru_cache(maxsize=1)
def get_aws_cloud_regions() -> set[str]:
    """
    Get AWS cloud regions.

    Returns:
        set[str]: The AWS cloud regions.

    References:
        AWS Regions: https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html#available-regions
    """
    url = 'https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html#available-regions'
    with urlopen(url=url) as response:  # noqa: S310
        content = response.read().decode('utf-8')

    pattern = r'<tr>\s*<td[^>]*tabindex="-1">(.*?)</td>\s*<td[^>]*tabindex="-1">.*?</td>\s*<td[^>]*tabindex="-1">.*?</td>\s*</tr>'  # noqa: E501
    region_codes = findall(pattern=pattern, string=content, flags=DOTALL)

    return {region_code.lower() for region_code in region_codes}


class AwsCloudRegionValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    AwsCloudRegionValueObject value object ensures the provided value is a valid AWS cloud region.

    References:
        AWS Regions: https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html#available-regions

    Example:
    ```python
    from value_object_pattern.usables.internet import AwsCloudRegionValueObject

    key = AwsCloudRegionValueObject(value='us-east-1')

    print(repr(key))
    # >>> AwsCloudRegionValueObject(value=us-east-1)
    ```
    """

    @process(order=0)
    def _ensure_region_is_in_lowercase(self, value: str) -> str:
        """
        Ensure AWS region is in lowercase.

        Args:
            value (str): The region value.

        Returns:
            str: The region value in lowercase.
        """
        return value.lower()

    @validation(order=0)
    def _validate_region(self, value: str) -> None:
        """
        Validate AWS region.

        Args:
            value (str): The region value.

        Raises:
            ValueError: If the region does not exist.
        """
        if value.lower() not in get_aws_cloud_regions():
            raise ValueError(f'AwsCloudRegionValueObject value <<<{value}>>> does not exist.')
