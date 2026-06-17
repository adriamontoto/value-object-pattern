from functools import lru_cache
from importlib.resources import files


@lru_cache(maxsize=1)
def get_iban_lengths() -> dict[str, int]:
    """
    Get IBAN lengths by country code.

    Returns:
        dict[str, int]: A ISO 3166-1 alpha-2 country code to with the IBAN length corresponds.

    References:
        IBAN Structure: https://www.iban.com/structure
    """
    lines = (
        files('value_object_pattern.usables.money.utils')
        .joinpath('iban_lengths.txt')
        .read_text(encoding='utf-8')
        .splitlines()
    )
    filtered_lines = tuple(line for line in lines if not line.startswith('#') and (_line := line.strip().upper()))

    return {line.split(', ')[0]: int(line.split(', ')[1]) for line in filtered_lines}
