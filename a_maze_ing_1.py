import sys
from mazegen.error import ConfigError
from mazegen import MazeGenerator
from print_maze import print_maze1, tema

def main() -> None:
	if len(sys.argv) != 2:
		print("Usage: python3 a_maze_ing.py <config_file>")
		sys.exit(1)

	try:
		generator = MazeGenerator(sys.argv[1])
		generator.generate()
		solution, path_coords = generator.solve()
		print_maze1(generator.grid, generator.entry, generator.exit, generator.width, generator.height, path_coords, None)
		color_index = -1
		flg = 1
		color_flg = 0
		color = None
		coor: list[tuple] = path_coords


		while True:
			solution, path_coords = generator.solve()
			if color_flg == 1:
				color = tema(color_index)
			maze_input = input(
				"=== A-Maze-ing ===\n"
				"1. Re-generate a new maze\n"
				"2. Show / Hide the shortest path\n"
				"3. Rotate the wall colours\n"
				"4. Quit\n"
				"\nChoice= (1-4): "
			)
			if flg == 1:
				flg = 0
				coor = []
			else:
				coor = path_coords
				flg = 1
			if maze_input == '1':
				generator.generate()
				solution, path_coords = generator.solve()
				coor = path_coords
				print_maze1(generator.grid, generator.entry, generator.exit, generator.width, generator.height, coor, color)
			elif maze_input == '2':
				print_maze1(generator.grid, generator.entry, generator.exit, generator.width, generator.height, coor, color)

			elif maze_input == '3':
				color_flg = 1
				if color_index > 4:
					color_index = 0
				else:
					color_index += 1
				print_maze1(generator.grid, generator.entry, generator.exit, generator.width, generator.height, coor, tema(color_index))

			elif maze_input == '4':
				break

			else:
				print("\n[!] Please choose a valid key\n")
				continue


	except (ConfigError, ValueError) as e:
		print(f"[ERROR]: ", e)
		sys.exit(1)


if __name__ == "__main__":
	main()