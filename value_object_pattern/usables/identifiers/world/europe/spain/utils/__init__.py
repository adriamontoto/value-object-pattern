from functools import lru_cache
from importlib.resources import files


@lru_cache(maxsize=1)
def get_provincial_codes() -> tuple[int, ...]:
    """
    Get provincial codes.

    Returns:
        tuple[int, ...]: The provincial codes.
    """
    with (
        files(anchor='value_object_pattern.usables.identifiers.world.europe.spain.utils')
        .joinpath('provincial_codes.txt')
        .open(mode='r') as file
    ):
        lines = file.read().splitlines()
        filtered_lines = tuple(int(line) for line in lines if not line.startswith('#') and (_line := line.strip()))

    return filtered_lines
