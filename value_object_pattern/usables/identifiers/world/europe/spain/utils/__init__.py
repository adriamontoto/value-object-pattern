from functools import lru_cache
from importlib.resources import files


@lru_cache(maxsize=1)
def get_provincial_codes() -> tuple[int, ...]:
    """
    Get provincial codes.

    Returns:
        tuple[int, ...]: The provincial codes.
    """
    lines = (
        files('value_object_pattern.usables.identifiers.world.europe.spain.utils')
        .joinpath('provincial_codes.txt')
        .read_text(encoding='utf-8')
        .splitlines()
    )
    filtered_lines = tuple(int(line) for line in lines if not line.startswith('#') and (_line := line.strip()))

    return filtered_lines
