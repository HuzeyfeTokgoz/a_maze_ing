"""Terminal rendering of a maze."""
from themes import RESET, Theme

Coord = tuple[int, int]

CLEAR_SCREEN = "\033[2J\033[H"


def _paint(text: str, color: str) -> str:
    """Return text wrapped in the given ANSI colour."""
    return f"{color}{text}{RESET}"


def _cell_content(cell: Coord, value: int, entry: Coord, exit: Coord,
                  path: set[Coord], theme: Theme) -> str:
    """Return the 3-character inside of a cell, already coloured."""
    if cell == entry:
        return _paint(" E ", theme.marker)
    if cell == exit:
        return _paint(" X ", theme.marker)
    if cell in path:
        return _paint(" * ", theme.path)
    if value == 15:
        return _paint("###", theme.pattern)
    return "   "


def print_maze(grid: list[list[int]], entry: Coord, exit: Coord,
               path_coords: list[Coord], theme: Theme) -> None:
    """Clear the terminal and draw the maze with the given theme.

    Args:
        grid: Maze cells, one wall bitmask per cell (N=1, E=2, S=4, W=8).
        entry: Entry cell, drawn as 'E'.
        exit: Exit cell, drawn as 'X'.
        path_coords: Cells of the shortest path; empty to hide it.
        theme: Colours used for walls, '42', path and markers.
    """
    path = set(path_coords)
    width = len(grid[0])

    print(CLEAR_SCREEN, end="")
    print(_paint("+" + "---+" * width, theme.wall))

    for y, row in enumerate(grid):
        middle = _paint("|", theme.wall)
        bottom = _paint("+", theme.wall)
        for x, value in enumerate(row):
            middle += _cell_content((x, y), value, entry, exit, path, theme)
            if value & 2:
                middle += _paint("|", theme.wall)
            else:
                middle += " "
            if value & 4:
                bottom += _paint("---+", theme.wall)
            else:
                bottom += _paint("   +", theme.wall)
        print(middle)
        print(bottom)
