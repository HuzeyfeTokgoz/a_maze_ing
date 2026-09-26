"""Entry point of A-Maze-ing: generate a maze and display it in a terminal."""
import sys

from mazegen import MazeGenerator
from mazegen.error import ConfigError
from print_maze import print_maze
from themes import THEMES, Theme

MENU = (
    "=== A-Maze-ing ===\n"
    "1. Re-generate a new maze\n"
    "2. Show / Hide the shortest path\n"
    "3. Rotate the colour theme\n"
    "4. Quit\n"
    "\nChoice (1-4): "
)


def render(generator: MazeGenerator, show_path: bool, theme: Theme) -> None:
    """Draw the maze, with or without the shortest path.

    Args:
        generator: Generator holding the maze to draw.
        show_path: Whether the shortest path is drawn.
        theme: Colour theme used for the drawing.
    """
    path = generator.path_coords if show_path else []
    print_maze(generator.grid, generator.entry, generator.exit, path, theme)
    print(f"Theme: {theme.name}")
    if not generator.pattern_cells:
        print("Warning: maze too small for the '42' pattern, skipped")


def run_menu(generator: MazeGenerator) -> None:
    """Run the interactive menu until the user quits.

    Args:
        generator: Generator whose maze is displayed and re-generated.
    """
    show_path = True
    theme_index = 0

    render(generator, show_path, THEMES[theme_index])
    while True:
        choice = input(MENU).strip()
        if choice == "1":
            generator.generate()
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            theme_index = (theme_index + 1) % len(THEMES)
        elif choice == "4":
            return
        else:
            print("\n[!] Please choose a valid key\n")
            continue
        render(generator, show_path, THEMES[theme_index])


def main() -> None:
    """Read the config file given on the command line and start the menu."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>", file=sys.stderr)
        sys.exit(1)

    try:
        generator = MazeGenerator(sys.argv[1])
        generator.generate()
        run_menu(generator)
    except (ConfigError, ValueError, RuntimeError) as e:
        print(f"[ERROR]: {e}", file=sys.stderr)
        sys.exit(1)
    except (KeyboardInterrupt, EOFError):
        print("\nBye!")


if __name__ == "__main__":
    main()
