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
    lines = (
        files('value_object_pattern.usables.internet.utils')
        .joinpath('aws_regions.txt')
        .read_text(encoding='utf-8')
        .splitlines()
    )
    filtered_lines = tuple(line for line in lines if not line.startswith('#') and (_line := line.strip().lower()))

    return filtered_lines


@lru_cache(maxsize=1)
def get_tld_dict() -> tuple[str, ...]:
    """
    Get top level domains from IANA in a dictionary.

    Returns:
        tuple[str, ...]: The top-level domains in lower case.

    References:
        TLD Domains: https://data.iana.org/TLD/tlds-alpha-by-domain.txt
    """
    lines = (
        files('value_object_pattern.usables.internet.utils')
        .joinpath('tld_domains.txt')
        .read_text(encoding='utf-8')
        .splitlines()
    )
    filtered_lines = tuple(line for line in lines if not line.startswith('#') and (_line := line.strip().lower()))

    return filtered_lines
