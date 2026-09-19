import sys
from parser import parse_config
from error import ConfigError
from mazegen import MazeGenerator
from writer import write_output

def main() -> None:
	if len(sys.argv) != 2:
		print("Usage: python3 a_maze_ing.py <config_file>")
		sys.exit(1)

	try:
		config = parse_config(sys.argv[1])
		generator = MazeGenerator(
			config.width,
			config.height,
			config.entry,
			config.exit,
			config.perfect,
			config.seed,
		)
	except (ConfigError, ValueError) as e:
		print(f"ERROR: ", e)
		sys.exit(1)

	if not generator.pattern_cells:
		print("Warning: maze too small for the '42' pattern, skipped")

	generator.generate()
	solution = generator.solve()

	try:
		write_output(config.output_file, generator.grid, config.entry,
			   config.exit, solution)

	except OSError as e:
		print(f"Error: cannot write '{config.output_file}': {e}")
		sys.exit(1)


if __name__ == "__main__":
	main()