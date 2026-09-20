from mazegen.error import ConfigError
from dataclasses import dataclass
 
MANDATORY_KEYS = [
	"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT",
]

@dataclass
class MazeConfig:
	"""Holds the values read from the configuration file."""

	width: int
	height: int
	entry: tuple[int, int]
	exit: tuple[int, int]
	output_file: str
	perfect: bool
	seed: int | None


def config_read(path):
	data: dict[str, str] = {}
	try:
		with open(path) as dosya:
			for number, line in enumerate(dosya, start=1):
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

	return data


def _parse_cell(key: str, value: str) -> tuple[int, int]:
	parts = value.split(",")
	if len(parts) != 2:
		raise ConfigError(f"{key} must be in 'x,y' format, got '{value}'")

	try:
		x, y = int(parts[0]), int(parts[1])
	except ValueError:
		raise ConfigError(f"{key} must contain integers, got '{value}'")

	return (x, y)


def _parse_int(key: str, value: str) -> int:
	"""Convert a string to an int or raise ConfigError."""
	try:
		return int(value)
	except ValueError:
		raise ConfigError(f"{key} must be an integer, got '{value}'")


def _parse_bool(key: str, value: str) -> bool:
    """Convert 'True' / 'False' (any case) to a bool."""
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    raise ConfigError(f"{key} must be True or False, got '{value}'")


def parse_config(path: str) -> MazeConfig:
	data = config_read(path)

	for key in MANDATORY_KEYS:
		if key not in data:
			raise ConfigError(f"missing mandatory key: {key}")

	seed = None
	if "SEED" in data:
		seed = _parse_int("SEED", data["SEED"])

	return MazeConfig(
		width=_parse_int("WIDTH", data["WIDTH"]),
		height=_parse_int("HEIGHT", data["HEIGHT"]),
		entry=_parse_cell("ENTRY", data["ENTRY"]),
		exit=_parse_cell("EXIT", data["EXIT"]),
		output_file=data["OUTPUT_FILE"],
		perfect=_parse_bool("PERFECT", data["PERFECT"]),
		seed=seed,
	)