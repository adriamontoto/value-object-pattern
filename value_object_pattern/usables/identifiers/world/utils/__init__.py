from functools import lru_cache
from importlib.resources import files


@lru_cache(maxsize=1)
def get_bcp47_language_subtags() -> tuple[str, ...]:
    """
    Get registered BCP 47 language subtags.

    Returns:
        tuple[str, ...]: Registered language subtags in lowercase.
    """
    lines = (
        files('value_object_pattern.usables.identifiers.world.utils')
        .joinpath('bcp47_language_subtags.txt')
        .read_text(encoding='utf-8')
        .splitlines()
    )

    return tuple(
        stripped_line.lower() for line in lines if not line.startswith('#') and (stripped_line := line.strip())
    )


@lru_cache(maxsize=1)
def get_bcp47_extlang_to_prefix_mapping() -> dict[str, str]:
    """
    Get registered BCP 47 extended-language subtags and their prefixes.

    Returns:
        dict[str, str]: Extended-language subtags mapped to their primary-language prefixes.
    """
    lines = (
        files('value_object_pattern.usables.identifiers.world.utils')
        .joinpath('bcp47_extlang_subtags.txt')
        .read_text(encoding='utf-8')
        .splitlines()
    )

    extlang_to_prefix = {}
    for line in lines:
        if not line.startswith('#') and (stripped_line := line.strip().lower()):
            extlang, prefix = stripped_line.split(maxsplit=1)
            extlang_to_prefix[extlang] = prefix

    return extlang_to_prefix


@lru_cache(maxsize=1)
def get_bcp47_script_subtags() -> tuple[str, ...]:
    """
    Get registered BCP 47 script subtags.

    Returns:
        tuple[str, ...]: Registered script subtags in lowercase.
    """
    lines = (
        files('value_object_pattern.usables.identifiers.world.utils')
        .joinpath('bcp47_script_subtags.txt')
        .read_text(encoding='utf-8')
        .splitlines()
    )

    return tuple(
        stripped_line.lower() for line in lines if not line.startswith('#') and (stripped_line := line.strip())
    )


@lru_cache(maxsize=1)
def get_bcp47_region_subtags() -> tuple[str, ...]:
    """
    Get registered BCP 47 region subtags.

    Returns:
        tuple[str, ...]: Registered region subtags in lowercase.
    """
    lines = (
        files('value_object_pattern.usables.identifiers.world.utils')
        .joinpath('bcp47_region_subtags.txt')
        .read_text(encoding='utf-8')
        .splitlines()
    )

    return tuple(
        stripped_line.lower() for line in lines if not line.startswith('#') and (stripped_line := line.strip())
    )


@lru_cache(maxsize=1)
def get_bcp47_variant_subtags() -> tuple[str, ...]:
    """
    Get registered BCP 47 variant subtags.

    Returns:
        tuple[str, ...]: Registered variant subtags in lowercase.
    """
    lines = (
        files('value_object_pattern.usables.identifiers.world.utils')
        .joinpath('bcp47_variant_subtags.txt')
        .read_text(encoding='utf-8')
        .splitlines()
    )

    return tuple(
        stripped_line.lower() for line in lines if not line.startswith('#') and (stripped_line := line.strip())
    )


@lru_cache(maxsize=1)
def get_bcp47_grandfathered_tag_mapping() -> dict[str, str]:
    """
    Get registered grandfathered BCP 47 tags.

    Returns:
        dict[str, str]: Lowercase tags mapped to their registered casing.
    """
    lines = (
        files('value_object_pattern.usables.identifiers.world.utils')
        .joinpath('bcp47_grandfathered_tags.txt')
        .read_text(encoding='utf-8')
        .splitlines()
    )

    tag_mapping = {}
    for line in lines:
        if not line.startswith('#') and (stripped_line := line.strip()):
            tag_mapping[stripped_line.lower()] = stripped_line

    return tag_mapping


@lru_cache(maxsize=1)
def get_bcp47_redundant_tag_mapping() -> dict[str, str]:
    """
    Get registered redundant BCP 47 tags.

    Returns:
        dict[str, str]: Lowercase tags mapped to their registered casing.
    """
    lines = (
        files('value_object_pattern.usables.identifiers.world.utils')
        .joinpath('bcp47_redundant_tags.txt')
        .read_text(encoding='utf-8')
        .splitlines()
    )

    tag_mapping = {}
    for line in lines:
        if not line.startswith('#') and (stripped_line := line.strip()):
            tag_mapping[stripped_line.lower()] = stripped_line

    return tag_mapping


@lru_cache(maxsize=1)
def get_iso3166_alpha2_codes() -> tuple[str, ...]:
    """
    Get ISO 3166-1 alpha-2 country codes.

    Returns:
        tuple[str, ...]: The ISO 3166-1 alpha-2 country codes in uppercase.

    References:
        ISO 3166-1 alpha-2 codes: https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
    """
    lines = (
        files('value_object_pattern.usables.identifiers.world.utils')
        .joinpath('iso3166_alpha2_codes.txt')
        .read_text(encoding='utf-8')
        .splitlines()
    )

    return tuple(line for line in lines if not line.startswith('#') and (_line := line.strip().upper()))


@lru_cache(maxsize=1)
def get_iso3166_alpha2_to_alpha3_mapping() -> tuple[dict[str, str], dict[str, str]]:
    """
    Get a mapping of ISO 3166-1 alpha-2 codes to alpha-3 codes and vice versa.

    Returns:
        tuple[dict[str, str], dict[str, str]]: A tuple containing two dictionaries, one for alpha-2 to alpha-3 mapping
        and another for alpha-3 to alpha-2 mapping.

    References:
        ISO 3166-1 alpha-2 to alpha-3 mapping: https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
    """
    lines = (
        files('value_object_pattern.usables.identifiers.world.utils')
        .joinpath('iso3166_alpha2_to_alpha3_mapping.txt')
        .read_text(encoding='utf-8')
        .splitlines()
    )

    alpha2_to_alpha3 = {}
    alpha3_to_alpha2 = {}
    for line in lines:
        if not line.startswith('#') and (stripped_line := line.strip()):
            alpha2, alpha3 = stripped_line.upper().split(sep=', ')
            alpha2_to_alpha3[alpha2] = alpha3
            alpha3_to_alpha2[alpha3] = alpha2

    return alpha2_to_alpha3, alpha3_to_alpha2


@lru_cache(maxsize=1)
def get_iso3166_alpha2_to_numeric_mapping() -> tuple[dict[str, int], dict[int, str]]:
    """
    Get a mapping of ISO 3166-1 alpha-2 codes to numeric codes and vice versa.

    Returns:
        tuple[dict[str, int], dict[int, str]]: A tuple containing two dictionaries, one for alpha-2 to numeric mapping
        and another for numeric to alpha-2 mapping.

    References:
        ISO 3166-1 alpha-2 to numeric mapping: https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
    """
    lines = (
        files('value_object_pattern.usables.identifiers.world.utils')
        .joinpath('iso3166_alpha2_to_numeric_mapping.txt')
        .read_text(encoding='utf-8')
        .splitlines()
    )

    alpha2_to_numeric = {}
    numeric_to_alpha2 = {}
    for line in lines:
        if not line.startswith('#') and (stripped_line := line.strip()):
            alpha2, numeric = stripped_line.upper().split(sep=', ')
            alpha2_to_numeric[alpha2] = int(numeric)
            numeric_to_alpha2[int(numeric)] = alpha2

    return alpha2_to_numeric, numeric_to_alpha2


@lru_cache(maxsize=1)
def get_iso3166_alpha2_to_phone_code_mapping() -> tuple[dict[str, str], dict[str, str]]:
    """
    Get a mapping of ISO 3166-1 alpha-2 codes to phone codes and vice versa.

    Returns:
        tuple[dict[str, str], dict[str, str]]: A tuple containing two dictionaries, one for alpha-2 to phone code
        mapping and another for phone code to alpha-2 mapping.

    References:
        ISO 3166-1 alpha-2 to phone code mapping: https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
    """
    lines = (
        files('value_object_pattern.usables.identifiers.world.utils')
        .joinpath('iso3166_alpha2_to_phone_code_mapping.txt')
        .read_text(encoding='utf-8')
        .splitlines()
    )

    alpha2_to_phone_code = {}
    phone_code_to_alpha2 = {}
    for line in lines:
        if not line.startswith('#') and (stripped_line := line.strip()):
            alpha2, phone_code = stripped_line.upper().split(sep=', ')
            alpha2_to_phone_code[alpha2] = phone_code
            phone_code_to_alpha2[phone_code] = alpha2

    return alpha2_to_phone_code, phone_code_to_alpha2


@lru_cache(maxsize=1)
def get_iso3166_alpha2_to_tld_mapping() -> tuple[dict[str, str], dict[str, str]]:
    """
    Get a mapping of ISO 3166-1 alpha-2 codes to TLDs and vice versa.

    Returns:
        tuple[dict[str, str], dict[str, str]]: A tuple containing two dictionaries, one for alpha-2 to TLD mapping
        and another for TLD to alpha-2 mapping.

    References:
        ISO 3166-1 alpha-2 to TLD mapping: https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
    """
    lines = (
        files('value_object_pattern.usables.identifiers.world.utils')
        .joinpath('iso3166_alpha2_to_tld_mapping.txt')
        .read_text(encoding='utf-8')
        .splitlines()
    )

    alpha2_to_tld = {}
    tld_to_alpha2 = {}
    for line in lines:
        if not line.startswith('#') and (stripped_line := line.strip()):
            alpha2, tld = stripped_line.split(sep=', ')
            alpha2, tld = alpha2.upper(), tld.lower()

            alpha2_to_tld[alpha2] = tld
            tld_to_alpha2[tld] = alpha2

    return alpha2_to_tld, tld_to_alpha2


@lru_cache(maxsize=1)
def get_iso3166_alpha3_codes() -> tuple[str, ...]:
    """
    Get ISO 3166-1 alpha-3 country codes.

    Returns:
        tuple[str, ...]: The ISO 3166-1 alpha-3 country codes in uppercase.

    References:
        ISO 3166-1 alpha-3 codes: https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
    """
    lines = (
        files('value_object_pattern.usables.identifiers.world.utils')
        .joinpath('iso3166_alpha3_codes.txt')
        .read_text(encoding='utf-8')
        .splitlines()
    )

    return tuple(line for line in lines if not line.startswith('#') and (_line := line.strip().upper()))


@lru_cache(maxsize=1)
def get_iso3166_numeric_codes() -> tuple[int, ...]:
    """
    Get ISO 3166-1 numeric country codes.

    Returns:
        tuple[int, ...]: The ISO 3166-1 numeric country codes.

    References:
        ISO 3166-1 numeric codes: https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
    """
    lines = (
        files('value_object_pattern.usables.identifiers.world.utils')
        .joinpath('iso3166_numeric_codes.txt')
        .read_text(encoding='utf-8')
        .splitlines()
    )

    return tuple(int(line) for line in lines if not line.startswith('#') and (_line := line.strip()))
