"""
AwsCloudRegionValueObject value object.
"""

from typing import NoReturn

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

    region = AwsCloudRegionValueObject(value='us-east-1')
    print(repr(region))
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
    def _validate_region(self, value: str, processed_value: str) -> None:
        """
        Validate AWS region.

        Args:
            value (str): The region value.
            processed_value (str): The early processed value.

        Raises:
            ValueError: If the region does not exist.
        """
        if processed_value not in get_aws_cloud_regions():
            self._raise_value_is_not_valid_aws_cloud_region(value=value)

    def _raise_value_is_not_valid_aws_cloud_region(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value is not a valid AWS cloud region.

        Args:
            value (str): The invalid AWS cloud region value.

        Raises:
            ValueError: If the value is not a valid AWS cloud region.
        """
        raise ValueError(f'AwsCloudRegionValueObject value <<<{value}>>> is not a valid AWS cloud region.')
