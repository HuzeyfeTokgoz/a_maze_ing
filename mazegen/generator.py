import random
from collections import deque
from .writer import write_output
from .parser import parse_config
from show import print_maze

Coord = tuple[int, int]


class MazeGenerator:

	DIRECTIONS: dict[str, tuple[int, str, int, int]] = {
	# name: (bit, opposite, dx, dy)
		"N": (1, "S", 0, -1),
		"E": (2, "W", 1, 0),
		"S": (4, "N", 0, 1),
		"W": (8, "E", -1, 0),
	}

	PATTERN_42: list[Coord] = [
		# 4
		(-3, -2), (-3, -1), (-3, 0), (-2, 0), (-1, 0), (-1, 1), (-1, 2),
		# 2
		(1, -2), (2, -2), (3, -2), (3, -1), (1, 0), (2, 0), (3, 0),
		(1, 1), (1, 2), (2, 2), (3, 2),
	]


	def __init__(self, file_path) -> None:
		config = parse_config(file_path)

		if config.width <= 0 or config.height <= 0:
			raise ValueError(
				f"maze size must be positive, got {config.width}x{config.height}")

		for name, (x, y) in (("ENTRY", config.entry), ("EXIT", config.exit)):
			if not (0 <= x < config.width and 0 <= y < config.height):
				raise ValueError(
					f"{name} ({x}, {y}) is outside the maze "
					f"({config.width}x{config.height})")

		if config.entry == config.exit:
			raise ValueError("ENTRY and EXIT must be different cells")

		self.file_path = file_path
		self.width = config.width
		self.height = config.height
		self.entry = config.entry
		self.exit = config.exit
		self.perfect = config.perfect
		self.output_file = config.output_file

		self._rnb_gen = random.Random(config.seed)
		self.grid: list[list[int]] = [[15] * self.width for _ in range(self.height)]
		self.pattern_cells = self._pattern_cells()
		self.solution: str = ""

		if not self.pattern_cells:
			print("Warning: maze too small for the '42' pattern, skipped")

		for name, cell in (("ENTRY", self.entry), ("EXIT", self.exit)):
			if cell in self.pattern_cells:
				raise ValueError(f"{name} {cell} is inside the '42' pattern")

	def _in_bounds(self, x: int, y: int) -> bool:
		"""Return True if (x, y) is inside the maze."""
		return 0 <= x < self.width and 0 <= y < self.height

	def _pattern_cells(self) -> set[Coord]:
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

	def _braid(self) -> None:
		for y, row in enumerate(self.grid):
			for x, cell in enumerate(row):
				counter = 0
				for _, (bit, _, _, _) in self.DIRECTIONS.items():
					if (cell & bit) != 0:
						counter += 1
				if counter == 3:
					closed: list[str] = []
					for direction, (bit, _, dx, dy) in self.DIRECTIONS.items():
						neig_x, neig_y = x + dx, y + dy
						if self._in_bounds(neig_x, neig_y):
							if((self.grid[y][x] & bit) != 0 and
		  						self.grid[neig_y][neig_x] != 15):
								closed.append(direction)
					if closed:
						self._remove_wall(x, y, self._rnb_gen.choice(closed))
					 
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
		if not self.perfect:
			self._braid()

		self.solution = self.solve()

	#	print_maze(self.grid, self.entry, self.exit, self.solution, self.pattern_cells)
		print_maze1(self.grid, self.entry, self.exit, self.width, self.height)
		try:
			write_output(self.output_file, self.grid, self.entry,
				self.exit, self.solution)
		except OSError as e:
			print(f"Error: cannot write '{self.output_file}': {e}")

	def solve(self) -> str:
		'''en kısa yolu buldurur bfs'''
		start = self.entry
		visited = {start} #
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
		cell = self.exit
		while cell != start:
			prev, direction = parent[cell]
			path.append(direction)
			cell = prev
		path.reverse()
		return "".join(path)


def print_maze1(grid, entry, finish, width, height):

	üst_satir = "+"
	for _ in range(width):
		üst_satir += "---+"
	print(üst_satir)

	for y in range(height):
		orta_satir = "|"
		alt_satir = "+"
		for x in range(width):
			hücre = (x, y)
			if hücre == entry:
				orta_satir += " E "
			elif hücre == finish:
				orta_satir += " X "
			
			elif grid[y][x] == 15:
				orta_satir += "#"

				
			else:
				orta_satir += "    "
			if grid[y][x] & 4:
				alt_satir += "---+"
			else:
				alt_satir += "   +"
		print(orta_satir)
		print(alt_satir)
