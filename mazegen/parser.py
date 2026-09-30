"""Read and check the A-Maze-ing configuration file."""
from dataclasses import dataclass

from .error import ConfigError

Coord = tuple[int, int]

MANDATORY_KEYS = [
    "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT",
]
MAX_SIZE = 50


@dataclass
class MazeConfig:
    """Holds the values read from the configuration file."""

    width: int
    height: int
    entry: Coord
    exit: Coord
    output_file: str
    perfect: bool
    seed: int | None


def config_read(path: str) -> dict[str, str]:
    """Read KEY=VALUE lines from a file into a dict.

    Empty lines and lines starting with '#' are skipped.

    Args:
        path: Path of the configuration file.

    Returns:
        The keys and values found in the file, as strings.

    Raises:
        ConfigError: If the file cannot be read or a line is invalid.
    """
    data: dict[str, str] = {}
    try:
        with open(path, encoding="utf-8") as file:
            for number, line in enumerate(file, start=1):
                line = line.strip()

                if not line or line.startswith('#'):
                    continue
                if "=" not in line:
                    raise ConfigError(f"line {number}: missing '='")

                key, value = line.split("=", 1)
                key = key.strip()

                if not key:
                    raise ConfigError(f"line {number}: empty key")
                if key in data:
                    raise ConfigError(f"line {number}: duplicate '{key}'")

                data[key] = value.strip()
    except OSError as e:
        raise ConfigError(f"Cannot read '{path}': {e}") from e
    except UnicodeDecodeError as e:
        raise ConfigError(f"'{path}' is not a valid text file") from e

    return data


def _parse_cell(key: str, value: str) -> Coord:
    """Convert an 'x,y' string to a coordinate.

    Args:
        key: Name of the key, used in error messages.
        value: Text to convert, e.g. "19,14".

    Returns:
        The coordinate (x, y).

    Raises:
        ConfigError: If the value is not two integers separated by a comma.
    """
    parts = value.split(",")
    if len(parts) != 2:
        raise ConfigError(f"{key} must be in 'x,y' format, got '{value}'")

    try:
        x, y = int(parts[0]), int(parts[1])
    except ValueError:
        raise ConfigError(f"{key} must contain integers, got '{value}'")

    return (x, y)


def _parse_int(key: str, value: str) -> int:
    """Convert a string to an int.

    Args:
        key: Name of the key, used in error messages.
        value: Text to convert.

    Returns:
        The integer value.

    Raises:
        ConfigError: If the value is not an integer.
    """
    try:
        return int(value)
    except ValueError:
        raise ConfigError(f"{key} must be an integer, got '{value}'")


def _parse_size(key: str, value: str) -> int:
    """Convert a maze size to an int between 1 and MAX_SIZE.

    Args:
        key: Name of the key (WIDTH or HEIGHT), used in error messages.
        value: Text to convert.

    Returns:
        The size.

    Raises:
        ConfigError: If the value is not an integer or is out of range.
    """
    size = _parse_int(key, value)
    if size < 1 or size > MAX_SIZE:
        raise ConfigError(
            f"{key} must be between 1 and {MAX_SIZE}, got {size}")
    return size


def _parse_bool(key: str, value: str) -> bool:
    """Convert 'True' / 'False' (any case) to a bool.

    Args:
        key: Name of the key, used in error messages.
        value: Text to convert.

    Returns:
        The boolean value.

    Raises:
        ConfigError: If the value is neither True nor False.
    """
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    raise ConfigError(f"{key} must be True or False, got '{value}'")


def parse_config(path: str) -> MazeConfig:
    """Read the configuration file and check its values.

    Args:
        path: Path of the configuration file.

    Returns:
        The checked configuration.

    Raises:
        ConfigError: If a key is missing or unknown, or a value is invalid.
    """
    data = config_read(path)

    for key in MANDATORY_KEYS:
        if key not in data:
            raise ConfigError(f"missing mandatory key: {key}")

    for key in data:
        if key not in MANDATORY_KEYS and key != "SEED":
            raise ConfigError(f"unknown key: {key}")

    seed = None
    if "SEED" in data:
        seed = _parse_int("SEED", data["SEED"])

    if data["OUTPUT_FILE"] == "":
        raise ConfigError("OUTPUT_FILE must not be empty")
    if data["OUTPUT_FILE"] == path:
        raise ConfigError("OUTPUT_FILE must not be the config file")

    return MazeConfig(
        width=_parse_size("WIDTH", data["WIDTH"]),
        height=_parse_size("HEIGHT", data["HEIGHT"]),
        entry=_parse_cell("ENTRY", data["ENTRY"]),
        exit=_parse_cell("EXIT", data["EXIT"]),
        output_file=data["OUTPUT_FILE"],
        perfect=_parse_bool("PERFECT", data["PERFECT"]),
        seed=seed,
    )
