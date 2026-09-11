import random
import sys
from collections import deque


def config_read(path):
	try:
		data = {}
		with open(path) as dosya:
			for line in dosya:
				line = line.strip()
				if not line or line.startswith('#'):
					continue
				if "=" in line:
					key, value = line.split("=", 1)
					data[key.strip()] = value.strip()
	except OSError as e:
		print(f"Config dosyasi okunamadi ({path}): {e}")
		return None
	else:
		return data


def parse_cell(data, key, width, height):
	''' Config'ten x,y koordinati okur, sinirlari dogrular '''
	try:
		x, y = map(int, data[key].split(','))
	except (KeyError, ValueError):
		print(f"{key} degeri gecersiz veya eksik (x,y formatinda olmali)")
		return None
	if not (0 <= x < width and 0 <= y < height):
		print(f"{key}={x},{y} labirent sinirlarinin disinda ({width}x{height})")
		return None
	return (x, y)


def config_write(maze_grid, data, roadmap):
	try:
		with open("maze.txt", "w", encoding="utf-8") as dosya:
			for row in maze_grid:
				hex_row = []
				for val in row:
					hex_char = format(val, 'X')
					hex_row.append(hex_char)
				line = "".join(hex_row)
				dosya.write(line + "\n")
			dosya.write("\n" + data["ENTRY"] + "\n")
			dosya.write(data["EXIT"] + "\n\n")
			road_line = "".join(roadmap)
			dosya.write(road_line)
	except Exception as e:
		print("Dosya yazılamadı", e)


def maze(data):
	''' Grid hazirlanmasi '''
	seed_val = data.get("SEED", 42)
	random.seed(seed_val)
	maze_grid = []

	for _ in range(int(data["HEIGHT"])):
		row = []
		for _ in range(int(data["WIDTH"])):
			row.append(15)
		maze_grid.append(row)
	return maze_grid


def visited_list(cell, maze_grid):
	x, y = cell

	visited = []
	for i in maze_grid:
		row = []
		for _ in i:
			row.append(False)
		visited.append(row)

	visited[y][x] = True
	return visited


def algorithm(data, maze_grid, cell, visited, directions):
	x, y = cell
	current_x, current_y = x, y
	stack = [(current_x, current_y)]

	while stack:
		neighbor: list[tuple[int, int, str]] = []

		for route, coor in directions.items():
			dx, dy = coor["coor"]
			neig_x: int = current_x + dx
			neig_y: int = current_y + dy

			if 0 <= neig_x < int(data["WIDTH"]) and 0 <= neig_y < int(data["HEIGHT"]):
				if not visited[neig_y][neig_x]:
					neighbor.append((neig_x, neig_y, route))

		if neighbor:
			ch_x, ch_y, ch_route = random.choice(neighbor)

			break_wall(maze_grid, directions, (current_x, current_y), ch_route)

			visited[ch_y][ch_x] = True
			stack.append((ch_x, ch_y))
			current_x, current_y = ch_x, ch_y
		else:
			stack.pop()
			if stack:
				current_x, current_y = stack[-1]


def break_wall(maze_grid, directions, cell, route):
	''' Verilen hucrenin verilen yondeki duvarini iki taraftan kirar '''
	x, y = cell
	dx, dy = directions[route]["coor"]
	opposite_route = directions[route]["opposite"]

	maze_grid[y][x] &= ~directions[route]["bit"]
	maze_grid[y + dy][x + dx] &= ~directions[opposite_route]["bit"]


def bfs(cell, maze_grid, data, directions):
	''' en kisa yolu bulma algoritmasi '''
	x, y = cell
	visited_lst = visited_list(cell, maze_grid)
	finish_x, finish_y = map(int, data["EXIT"].split(','))
	queue = deque([(x, y)])
	parent = {(x, y): None}
	finded = False

	while queue:
		current_x, current_y = queue.popleft()

		if current_x == finish_x and current_y == finish_y:
			finded = True
			break
		cell_value = maze_grid[current_y][current_x]

		for route, coor in directions.items():
			dx, dy = coor["coor"]
			bit = coor["bit"]
			new_x, new_y = current_x + dx, current_y + dy

			if 0 <= new_x < int(data["WIDTH"]) and 0 <= new_y < int(data["HEIGHT"]):
				if not visited_lst[new_y][new_x]:
					if (cell_value & bit) == 0:
						visited_lst[new_y][new_x] = True
						parent[(new_x, new_y)] = ((current_x, current_y), route[0].upper())
						queue.append((new_x, new_y))

	path_coords = set() #
	path_letters = []
	if finded:
		curr = (finish_x, finish_y)
		while parent[curr] is not None:
			prev_cell, letter = parent[curr]
			path_letters.append(letter)
			curr = prev_cell
			path_coords.add(curr) #
		path_letters.reverse()
	print_maze(maze_grid, path_coords)
	return path_letters

def grid_analyzer(maze_grid, data, directions):
	for y, row in enumerate(maze_grid):
		for x, grid_cell in enumerate(row):
			counter = 0
			for bit in [1, 2, 4, 8]:
				if (grid_cell & bit) != 0:
					counter += 1
			if counter == 3:
				closed: list[str] = []

				for route, coor in directions.items():
					dx, dy = coor["coor"]
					neig_x = x + dx
					neig_y = y + dy

					if 0 <= neig_x < int(data["WIDTH"]) and 0 <= neig_y < int(data["HEIGHT"]):
						if (maze_grid[y][x] & coor["bit"]) != 0 and maze_grid[neig_y][neig_x] != 15:
							closed.append(route)

				if closed:
					break_wall(maze_grid, directions, (x, y), random.choice(closed))

def ft_pattern(data, maze_grid, visited):
	''' "42" desenini olusturacak hucreleri tam kapali birakir '''
	width = int(data["WIDTH"])
	height = int(data["HEIGHT"])
	center_x = width // 2
	center_y = height // 2

	four_pattern = [
		(center_x - 3, center_y - 2),
		(center_x - 3, center_y - 1),
		(center_x - 3, center_y),
		(center_x - 2, center_y),
		(center_x - 1, center_y),
		(center_x - 1, center_y + 1),
		(center_x - 1, center_y + 2),
	]

	two_pattern = [
		(center_x + 1, center_y - 2),
		(center_x + 2, center_y - 2),
		(center_x + 3, center_y - 2),
		(center_x + 3, center_y - 1),
		(center_x + 1, center_y),
		(center_x + 2, center_y),
		(center_x + 3, center_y),
		(center_x + 1, center_y + 1),
		(center_x + 1, center_y + 2),
		(center_x + 2, center_y + 2),
		(center_x + 3, center_y + 2),
	]

	pattern = four_pattern + two_pattern

	if center_x - 3 < 1 or center_x + 3 > width - 2 or center_y - 2 < 1 or center_y + 2 > height - 2:
		print("'42' deseni icin labirent cok kucuk, desen atlandi")
		return

	for x, y in pattern:
		maze_grid[y][x] = 15
		visited[y][x] = True


def print_maze(maze_grid, path_coords=None):
    if path_coords is None:
        path_coords = set()
        
    height = len(maze_grid)
    width = len(maze_grid[0])
    
    print("+" + "---+" * width)
    
    for y in range(height):
        line = "|"
        for x in range(width):
            cell = maze_grid[y][x]
            
            if (x, y) in path_coords:
                center = " * "
            else:
                center = "   "
                
            bottom = "___" if (cell & 4) else center
            right = "|" if (cell & 2) else " "
            line += bottom + right
        print(line)


def main():
	directions: dict[str, dict[str, any]] = {
		"North":{"bit": 1, "opposite": "South", "coor": (0, -1)},
		"East":{"bit": 2, "opposite": "West", "coor": (+1, 0)},
		"South":{"bit": 4, "opposite": "North", "coor": (0, +1)},
		"West":{"bit": 8, "opposite": "East", "coor": (-1, 0)}
	}

	data = config_read()
	if not data:
		return

	maze_grid = maze(data)
	x, y = map(int, data["ENTRY"].split(','))
	cell = ((x, y))

	visited_lst = visited_list(cell, maze_grid)
	ft_pattern(data, maze_grid, visited_lst)

	algorithm(data, maze_grid, cell, visited_lst, directions)

	if data.get("PERFECT", "True").strip().lower() not in ("true", "1", "yes"):
		grid_analyzer(maze_grid, data, directions)

	path_letters = bfs(cell, maze_grid, data, directions)
	config_write(maze_grid, data, path_letters)

if __name__ == "__main__":
	main()