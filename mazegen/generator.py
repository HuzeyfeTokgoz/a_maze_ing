import random
from collections import deque

class MazeGenerator:

	DIRECTIONS: dict[str, tuple[int, str, int, int]] = {
	# name: (bit, opposite, dx, dy)
		"N": (1, "S", 0, -1),
		"E": (2, "W", 1, 0),
		"S": (4, "N", 0, 1),
		"W": (8, "E", -1, 0),
	}

	PATTERN_42: list[tuple[int, int]] = [
		# 4
		(-3, -2), (-3, -1), (-3, 0), (-2, 0), (-1, 0), (-1, 1), (-1, 2),
		# 2
		(1, -2), (2, -2), (3, -2), (3, -1), (1, 0), (2, 0), (3, 0),
		(1, 1), (1, 2), (2, 2), (3, 2),
	]

	def __init__(self, width: int, height: int, entry: tuple[int, int],
			  exit: tuple[int, int], perfect: bool = False,
				seed: int | None = None) -> None:

		if width <= 0 or height <= 0:
			raise ValueError(
				f"maze size must be positive, got {width}x{height}")

		for name, (x, y) in (("ENTRY", entry), ("EXIT", exit)):
			if not (0 <= x < width and 0 <= y < height):
				raise ValueError(
					f"{name} ({x}, {y}) is outside the maze "
					f"({width}x{height})")

		if entry == exit:
			raise ValueError("ENTRY and EXIT must be different cells")

		self.width = width
		self.height = height
		self.entry = entry
		self.exit = exit
		self.perfect = perfect
		self._rnb_gen = random.Random(seed)
		self.grid: list[list[int]] = [[15] * width for _ in range(height)]
		self.pattern_cells = self._pattern_cells()

		for name, cell in (("ENTRY", entry), ("EXIT", exit)):
			if cell in self.pattern_cells:
				raise ValueError(f"{name} {cell} is inside the '42' pattern")

	def _in_bounds(self, x: int, y: int) -> bool:
		"""Return True if (x, y) is inside the maze."""
		return 0 <= x < self.width and 0 <= y < self.height

	def _pattern_cells(self) -> set[tuple[int, int]]:
		cx, cy = self.width // 2, self.height // 2
		if (cx - 3 < 1 or cx + 3 > self.width - 2
				or cy - 2 < 1 or cy + 2 > self.height - 2):
			return set()
		return {(cx + dx, cy + dy) for dx, dy in self.PATTERN_42}

	def _remove_wall(self, x: int, y: int, direction: str) -> None:
		bit, opposite, dx, dy = self.DIRECTIONS[direction]
		opposite_bit = self.DIRECTIONS[opposite][0]
		self.grid[y][x] &= ~bit
		self.grid[y + dy][x + dx] &= ~opposite_bit

	def _carve(self, visited: list[list[bool]]) -> None:
		start_x, start_y = self.entry
		visited[start_y][start_x] = True
		stack = [self.entry]

		while stack:
			x, y = stack[-1]
			neig: list[tuple[int, int, str]] = []
			for direction, (_, _, dx, dy) in self.DIRECTIONS.items():
				new_x, new_y = x + dx, y + dy
				if self._in_bounds(new_x, new_y) and not visited[new_y][new_x]:
					neig.append((new_x, new_y, direction))

			if neig:
				new_x, new_y, direction = self._rnb_gen.choice(neig)
				self._remove_wall(x, y, direction)
				visited[new_y][new_x] = True
				stack.append((new_x, new_y))
			else:
				stack.pop()

	def generate(self) -> None:
		self.grid = [[15] * self.width for _ in range(self.height)]

		visited = [[False] * self.width for _ in range(self.height)]
		for x, y in self.pattern_cells:
			visited[y][x] = True

		self._carve(visited)

	def solve(self) -> str:
		'''en kısa yolu buldurur bfs'''
		start = self.entry
		visited = {start} #
		parent: dict[tuple[int, int], tuple[int, int, str]] = {}
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
		cell = self.exit
		while cell != start:
			prev, direction = parent[cell]
			path.append(direction)
			cell = prev
		path.reverse()
		return "".join(path)