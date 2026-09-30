"""Terminal rendering of a maze."""
from themes import RESET, Theme

CLEAR_SCREEN = "\033[H\033[2J\033[3J"
Coord = tuple[int, int]


def _paint(text: str, color: str) -> str:
    """Wrap text in an ANSI colour.

    Args:
        text: Text to colour.
        color: ANSI escape code of the colour.

    Returns:
        The coloured text, followed by a reset code.
    """
    return f"{color}{text}{RESET}"


def _cell_content(cell: Coord, value: int, entry: Coord, exit: Coord,
                  path: set[Coord], theme: Theme) -> str:
    """Build the 3-character inside of a cell.

    Args:
        cell: Coordinates (x, y) of the cell.
        value: Wall bitmask of the cell; 15 means a '42' cell.
        entry: Entry cell, drawn as 'E'.
        exit: Exit cell, drawn as 'X'.
        path: Cells of the shortest path, drawn as '*'.
        theme: Colours to use.

    Returns:
        The coloured inside of the cell, or 3 spaces for an empty cell.
    """
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
