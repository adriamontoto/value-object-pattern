from functools import lru_cache


@lru_cache(maxsize=1)
def get_iso3166_alpha2_codes() -> tuple[str, ...]:
    """
    Get ISO 3166-1 alpha-2 country codes.

    Returns:
        tuple[str, ...]: The ISO 3166-1 alpha-2 country codes in uppercase.

    References:
        ISO 3166-1 alpha-2 codes: https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
    """
    with open(file='value_object_pattern/usables/identifiers/countries/utils/iso3166_alpha2_codes.txt') as file:
        lines = file.read().splitlines()
        filtered_lines = tuple(line for line in lines if not line.startswith('#') and (_line := line.strip().upper()))

    return filtered_lines
