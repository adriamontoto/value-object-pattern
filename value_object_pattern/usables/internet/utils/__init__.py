from functools import lru_cache
from importlib.resources import files


@lru_cache(maxsize=1)
def get_aws_cloud_regions() -> tuple[str, ...]:
    """
    Get AWS cloud regions from the official AWS documentation.

    Returns:
        tuple[str, ...]: The AWS regions in lower case.

    References:
        AWS Cloud Regions: https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html#available-regions
    """
    with files(anchor='value_object_pattern.usables.internet.utils').joinpath('aws_regions.txt').open(mode='r') as file:
        lines = file.read().splitlines()
        filtered_lines = tuple(line for line in lines if not line.startswith('#') and (_line := line.strip().lower()))

    return filtered_lines
