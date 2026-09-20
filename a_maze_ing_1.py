import sys
from mazegen.error import ConfigError
from mazegen import MazeGenerator


def main() -> None:
	if len(sys.argv) != 2:
		print("Usage: python3 a_maze_ing.py <config_file>")
		sys.exit(1)

	try:
		generator = MazeGenerator(sys.argv[1])
		generator.generate()

	except (ConfigError, ValueError) as e:
		print(f"[ERROR]: ", e)
		sys.exit(1)


if __name__ == "__main__":
	main()