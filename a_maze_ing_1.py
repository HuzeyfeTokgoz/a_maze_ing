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


		while True:
			maze_input = input(
				"=== A-Maze-ing ===\n"
				"1. Re-generate a new maze\n"
				"2. Show / Hide the shortest path\n"
				"3. Rotate the wall colours\n"
				"4. Quit\n"
				"Choice= (1-4): "
			)
			if maze_input == '1':
				generator.generate()
			elif maze_input == '2':
				#yol aç kapa
				pass
			elif maze_input == '3':
				#color
				pass
			elif maze_input == '4':
				break
			else:
				print("\n! Please choose a valid key\n")
				continue

	except (ConfigError, ValueError) as e:
		print(f"[ERROR]: ", e)
		sys.exit(1)


if __name__ == "__main__":
	main()