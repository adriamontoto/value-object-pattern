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


@lru_cache(maxsize=1)
def get_tld_dict() -> dict[int, tuple[str, ...]]:
    """
    Get top level domains from IANA in a dictionary sorted by domain length.

    Returns:
        dict[int, tuple[str, ...]]: The top level domains in lower case sorted by domain length.

    References:
        TLD Domains: https://data.iana.org/TLD/tlds-alpha-by-domain.txt
    """
    with files(anchor='value_object_pattern.usables.internet.utils').joinpath('tld_domains.txt').open(mode='r') as file:
        lines = file.read().splitlines()

    temp: dict[int, list[str]] = {}
    tlds = tuple(line for line in lines if not line.startswith('#') and (_line := line.strip().lower()))
    for tld in tlds:
        key = len(tld)
        temp.setdefault(key, []).append(tld)

    return {key: tuple(value) for key, value in temp.items()}

