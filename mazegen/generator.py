"""Maze generation: depth-first carving, braiding and BFS solving."""
import random
from collections import deque

from .parser import Coord, parse_config
from .writer import write_output


class MazeGenerator:
    """Generate a maze on a grid of cells and find its shortest path.

    Each cell is an int whose bits are its closed walls:
    North = 1, East = 2, South = 4, West = 8 (15 = all walls closed).

    Example:
        >>> generator = MazeGenerator("config.txt")
        >>> generator.generate()      # also writes OUTPUT_FILE
        >>> generator.grid[0][0]      # walls of the top-left cell
        >>> generator.solution        # shortest path, e.g. "EESSW..."

    Attributes:
        width: Number of columns.
        height: Number of rows.
        entry: Entry cell (x, y).
        exit: Exit cell (x, y).
        perfect: True for a single path between any two cells.
        output_file: File written by generate().
        grid: Wall bitmask of every cell, indexed as grid[y][x].
        pattern_cells: Fully closed cells drawing the '42' (may be empty).
        solution: Shortest path from entry to exit as N/E/S/W letters.
        path_coords: Cells of the shortest path, from entry to exit.
    """

    # name: (bit, opposite, dx, dy)
    DIRECTIONS: dict[str, tuple[int, str, int, int]] = {
        "N": (1, "S", 0, -1),
        "E": (2, "W", 1, 0),
        "S": (4, "N", 0, 1),
        "W": (8, "E", -1, 0),
    }

    PATTERN_42: list[Coord] = [
        # 4
        (-3, -2), (-3, -1), (-3, 0), (-2, 0), (-1, 0), (-1, 1), (-1, 2),
        (-1, -2), (-1, -1),
        # 2
        (1, -2), (2, -2), (3, -2), (3, -1), (1, 0), (2, 0), (3, 0),
        (1, 1), (1, 2), (2, 2), (3, 2),
    ]

    MIN_LOOP_SIZE = 5

    def __init__(self, path: str) -> None:
        """Read the configuration file and prepare an empty maze.

        Args:
            path: Path of the configuration file (WIDTH, HEIGHT, ENTRY,
                EXIT, OUTPUT_FILE, PERFECT and optional SEED).

        Raises:
            ConfigError: If the file cannot be read or a value is invalid.
            ValueError: If the entry or exit is invalid, or the maze is
                too small for loops when PERFECT is False.
        """
        config = parse_config(path)
        width, height = config.width, config.height

        size = self.MIN_LOOP_SIZE
        if not config.perfect and (width < size or height < size):
            raise ValueError(
                f"PERFECT=False needs a maze of at least {size}x{size}, "
                f"got {width}x{height}")

        for name, (x, y) in (("ENTRY", config.entry), ("EXIT", config.exit)):
            if not (0 <= x < width and 0 <= y < height):
                raise ValueError(
                    f"{name} ({x}, {y}) is outside the maze "
                    f"({width}x{height})")

        if config.entry == config.exit:
            raise ValueError("ENTRY and EXIT must be different cells")

        self.width = width
        self.height = height
        self.entry = config.entry
        self.exit = config.exit
        self.perfect = config.perfect
        self.output_file = config.output_file

        self._rng = random.Random(config.seed)
        self.grid = self._new_grid()
        self.pattern_cells = self._pattern_cells()
        self.path_coords: list[Coord] = []
        self.solution: str = ""

        for name, cell in (("ENTRY", self.entry), ("EXIT", self.exit)):
            if cell in self.pattern_cells:
                raise ValueError(f"{name} {cell} is inside the '42' pattern")

    def _new_grid(self) -> list[list[int]]:
        """Return a grid where every cell has its 4 walls closed."""
        grid: list[list[int]] = []
        for _ in range(self.height):
            grid.append([15] * self.width)
        return grid

    def _in_bounds(self, x: int, y: int) -> bool:
        """Return True if (x, y) is inside the maze."""
        return 0 <= x < self.width and 0 <= y < self.height

    def _pattern_cells(self) -> set[Coord]:
        """Return the cells of the '42', or an empty set if it does not fit."""
        cx, cy = self.width // 2, self.height // 2
        if (cx - 3 < 1 or cx + 3 > self.width - 2
                or cy - 2 < 1 or cy + 2 > self.height - 2):
            return set()

        cells: set[Coord] = set()
        for dx, dy in self.PATTERN_42:
            cells.add((cx + dx, cy + dy))
        return cells

    def _remove_wall(self, x: int, y: int, direction: str) -> None:
        """Open the wall of (x, y) in a direction, on both sides."""
        bit, opposite, dx, dy = self.DIRECTIONS[direction]
        opposite_bit = self.DIRECTIONS[opposite][0]

        self.grid[y][x] &= ~bit
        self.grid[y + dy][x + dx] &= ~opposite_bit

    def _braid(self) -> None:
        """Remove dead-ends by opening one more wall of each of them.

        A dead-end is a cell with 3 closed walls. Walls towards the border
        or towards the '42' are never opened.
        """
        for y in range(self.height):
            for x in range(self.width):
                counter = 0
                for bit, _, _, _ in self.DIRECTIONS.values():
                    if (self.grid[y][x] & bit) != 0:
                        counter += 1

                if counter == 3:
                    closed: list[str] = []
                    for direction, (bit, _, dx, dy) in self.DIRECTIONS.items():
                        neig_x = x + dx
                        neig_y = y + dy
                        if not self._in_bounds(neig_x, neig_y):
                            continue
                        if (neig_x, neig_y) in self.pattern_cells:
                            continue
                        if (self.grid[y][x] & bit) != 0:
                            closed.append(direction)

                    if closed:
                        self._remove_wall(x, y, self._rng.choice(closed))

    def _carve(self, visited: list[list[bool]]) -> None:
        """Carve a perfect maze from the entry with a depth-first search."""
        start_x, start_y = self.entry
        visited[start_y][start_x] = True
        stack = [self.entry]

        while stack:
            x, y = stack[-1]
            neig: list[tuple[int, int, str]] = []
            for direction, (_, _, dx, dy) in self.DIRECTIONS.items():
                new_x, new_y = x + dx, y + dy
                if (self._in_bounds(new_x, new_y)
                        and not visited[new_y][new_x]):
                    neig.append((new_x, new_y, direction))

            if neig:
                new_x, new_y, direction = self._rng.choice(neig)
                self._remove_wall(x, y, direction)
                visited[new_y][new_x] = True
                stack.append((new_x, new_y))
            else:
                stack.pop()

    def generate(self) -> None:
        """Build a new maze, store it with its shortest path and write it.

        Every call gives a different maze; the sequence of mazes is the
        same for a given seed.

        Raises:
            OSError: If the output file cannot be written.
        """
        self.grid = self._new_grid()
        visited = [[False] * self.width for _ in range(self.height)]

        for x, y in self.pattern_cells:
            visited[y][x] = True

        self._carve(visited)
        if not self.perfect:
            self._braid()

        self.solution, self.path_coords = self.solve()
        write_output(self.output_file, self.grid, self.entry, self.exit,
                     self.solution)

    def solve(self) -> tuple[str, list[Coord]]:
        """Find the shortest path from entry to exit with a BFS.

        Returns:
            The path as N/E/S/W letters, and its cells from entry to exit.

        Raises:
            RuntimeError: If the exit cannot be reached.
        """
        start = self.entry
        visited = {start}
        parent: dict[Coord, tuple[Coord, str]] = {}
        queue = deque([start])

        while queue:
            x, y = queue.popleft()
            if (x, y) == self.exit:
                break
            for direction, (bit, _, dx, dy) in self.DIRECTIONS.items():
                if self.grid[y][x] & bit:
                    continue
                next_cell = (x + dx, y + dy)
                if next_cell not in visited:
                    visited.add(next_cell)
                    parent[next_cell] = ((x, y), direction)
                    queue.append(next_cell)
        if self.exit not in visited:
            raise RuntimeError(
                "exit is not reachable (was generate() called?)")

        path: list[str] = []
        path_coords: list[Coord] = [self.exit]
        cell = self.exit
        while cell != start:
            prev, direction = parent[cell]
            path.append(direction)
            path_coords.append(prev)
            cell = prev
        path.reverse()
        path_coords.reverse()
        return "".join(path), path_coords
