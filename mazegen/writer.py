"""Write a maze to a file in the hexadecimal output format."""


def write_output(filename: str, grid: list[list[int]], entry: tuple[int, int],
                 exit: tuple[int, int], solution: str) -> None:
    """Write the maze, its entry, exit and shortest path to a file.

    Each cell is written as one hexadecimal digit (N=1, E=2, S=4, W=8),
    one row per line. After an empty line come the entry, the exit and
    the path as N/E/S/W letters.

    Args:
        filename: Path of the output file.
        grid: Maze cells, one wall bitmask per cell.
        entry: Entry coordinates (x, y).
        exit: Exit coordinates (x, y).
        solution: Shortest path from entry to exit, e.g. "EESN".

    Raises:
        OSError: If the file cannot be written.
    """
    with open(filename, "w", encoding="utf-8") as file:
        for row in grid:
            line = ""
            for cell in row:
                line += format(cell, "x")
            file.write(line + "\n")

        file.write("\n")
        file.write(f"{entry[0]},{entry[1]}\n")
        file.write(f"{exit[0]},{exit[1]}\n")
        file.write(solution + "\n")
