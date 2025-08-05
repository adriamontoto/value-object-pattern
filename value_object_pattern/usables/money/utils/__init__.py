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
    with files(anchor='value_object_pattern.usables.money.utils').joinpath('iban_lengths.txt').open(mode='r') as file:
        lines = file.read().splitlines()
        filtered_lines = tuple(line for line in lines if not line.startswith('#') and (_line := line.strip().upper()))

    return {line.split(', ')[0]: int(line.split(', ')[1]) for line in filtered_lines}
