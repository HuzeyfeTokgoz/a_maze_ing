# mazegen

Reusable maze generator from the A-Maze-ing project.
It builds a maze with a depth-first search, can add loops to it, and finds
the shortest path from the entry to the exit with a breadth-first search.

## Install

```
pip install mazegen-1.0.0-py3-none-any.whl
```

## Basic example

```python
from mazegen import MazeGenerator

generator = MazeGenerator(20, 15, (0, 0), (19, 14))
generator.generate()

print(generator.solution)   # shortest path, e.g. "EESSWS..."
```

## Custom parameters

```python
MazeGenerator(width, height, entry, exit, perfect=False, seed=None)
```

| Parameter | Meaning |
|-----------|---------|
| `width`, `height` | Size of the maze, in cells |
| `entry`, `exit` | `(x, y)` cells, inside the maze and different |
| `perfect` | `True`: exactly one path between two cells. `False` (default): a maze with loops, at least 5x5 |
| `seed` | Same seed gives the same mazes. `None` gives a random maze |

Invalid parameters raise `ValueError`.
Calling `generate()` again builds a new maze.

## Access the maze and the solution

- `generator.grid`: list of rows, `grid[y][x]` is the cell at `(x, y)`.
  Each cell is an int whose bits are its closed walls:
  North = 1, East = 2, South = 4, West = 8 (15 = all walls closed).
- `generator.solution`: shortest path as a string of `N`, `E`, `S`, `W`.
- `generator.path_coords`: cells of the shortest path, from entry to exit.
- `generator.pattern_cells`: closed cells drawing the "42"
  (empty when the maze is too small for it).

## Config file and output file (optional)

```python
from mazegen import ConfigError, MazeGenerator, parse_config, write_output

config = parse_config("config.txt")      # raises ConfigError if invalid
generator = MazeGenerator(config.width, config.height, config.entry,
                          config.exit, config.perfect, config.seed)
generator.generate()
write_output(config.output_file, generator.grid, generator.entry,
             generator.exit, generator.solution)
```
