from functools import lru_cache
from importlib.resources import files


@lru_cache(maxsize=1)
def get_provincial_plate_codes() -> tuple[str, ...]:
    """
    Get provincial plate codes from the official Spanish vehicle registration documentation.

    Returns:
        tuple[str, ...]: The provincial plate codes in upper case.
    """
    with (
        files(anchor='value_object_pattern.usables.identifiers.world.europe.spain.plates.utils')
        .joinpath('provincial_plate_codes.txt')
        .open(mode='r') as file
    ):
        lines = file.read().splitlines()
        filtered_lines = tuple(line for line in lines if not line.startswith('#') and (_line := line.strip().upper()))

    return filtered_lines
