"""
AwsCloudRegionValueObject value object.
"""

from value_object_pattern import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .utils import get_aws_cloud_regions


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

    @validation(order=0, early_process=True)
    def _validate_region(self, value: str) -> None:
        """
        Validate AWS region.

        Args:
            value (str): The region value.

        Raises:
            ValueError: If the region does not exist.
        """
        if value not in get_aws_cloud_regions():
            raise ValueError(f'AwsCloudRegionValueObject value <<<{value}>>> does not exist.')
