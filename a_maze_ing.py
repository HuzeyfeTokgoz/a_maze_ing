"""Entry point of A-Maze-ing: generate a maze and display it in a terminal."""
import sys

from mazegen import ConfigError, MazeGenerator, parse_config, write_output
from print_maze import print_maze
from themes import THEMES


def new_maze(generator: MazeGenerator, output_file: str) -> None:
    """Generate a new maze and write it to the output file."""
    generator.generate()
    write_output(output_file, generator.grid, generator.entry,
                 generator.exit, generator.solution)


def draw_maze(generator: MazeGenerator, show_path: bool,
              theme_index: int) -> None:
    """Draw the maze with the chosen theme, with or without the path."""
    if show_path:
        path = generator.path_coords
    else:
        path = []
    print_maze(generator.grid, generator.entry, generator.exit,
               path, THEMES[theme_index])

    if not generator.pattern_cells:
        print("Warning: maze too small for the '42' pattern, skipped")


def main() -> None:
    """Read the config file, generate the maze and run the menu."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)

    try:
        config = parse_config(sys.argv[1])
        generator = MazeGenerator(config.width, config.height, config.entry,
                                  config.exit, config.perfect, config.seed)
        new_maze(generator, config.output_file)

        show_path = True
        theme_index = 0
        draw_maze(generator, show_path, theme_index)

        while True:
            choice = input("=== A-Maze-ing ===\n"
                           "1. Re-generate a new maze\n"
                           "2. Show / Hide the shortest path\n"
                           "3. Rotate the colour theme\n"
                           "4. Quit\n"
                           "\nChoice (1-4): ").strip()

            if choice == "1":
                new_maze(generator, config.output_file)
            elif choice == "2":
                show_path = not show_path
            elif choice == "3":
                theme_index = (theme_index + 1) % len(THEMES)
            elif choice == "4":
                break
            else:
                print("\n[!] Please choose a valid key\n")
                continue

            draw_maze(generator, show_path, theme_index)

    except (ConfigError, ValueError, RuntimeError, OSError) as e:
        print(f"[ERROR]: {e}")
        sys.exit(1)
    except (KeyboardInterrupt, EOFError):
        print("\nBye!")


if __name__ == "__main__":
    main()
