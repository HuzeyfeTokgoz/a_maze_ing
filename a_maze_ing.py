import random
from collections import deque


def config_read():
	try:
		data = {}
		with open("config.txt") as dosya:
			for line in dosya:
				if not line or line.startswith('#'):
					continue
				if "=" in line:
					key, value = line.split("=", 1)
					data[key.strip()] = value.strip()
	except Exception:
		print("Dosya bulunamadı")
		return None
	else:
		return data


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
			dosya.write("\nENTRY= " + data["ENTRY"])
			dosya.write("\nEXIT= " + data["EXIT"] + "\n\n")
			road_line = "".join(roadmap)
			dosya.write(road_line)
	except Exception as e:
		print("Dosya yazılamadı", e)


def maze(data):
	seed_val = data.get("SEED", 42)
	random.seed(seed_val)
	maze_grid = []

	for _ in range(int(data["HEIGHT"])):
		row = []
		for _ in range(int(data["WIDTH"])):
			row.append(15)
		maze_grid.append(row)
	return maze_grid


def visited_list(y, x, maze_grid):
	visited = []
	for i in maze_grid:
		row = []
		for _ in i:
			row.append(False)
		visited.append(row)

	visited[y][x] = True
	return visited


def algorithm():
	data = config_read()
	maze_grid = maze(data)
	x, y = map(int, data["ENTRY"].split(','))
	current_x, current_y = x, y

	visited = visited_list(y, x, maze_grid)
	stack = [(current_x, current_y)]

	directions: dict[str, dict[str, any]] = {
		"North":{"bit": 1, "opposite": "South", "coor": (0, -1)},
		"East":{"bit": 2, "opposite": "West", "coor": (+1, 0)},
		"South":{"bit": 4, "opposite": "North", "coor": (0, +1)},
		"West":{"bit": 8, "opposite": "East", "coor": (-1, 0)}
	}

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

			### duvar kırma ###
			current_bit = directions[ch_route]["bit"]
			maze_grid[current_y][current_x] &= ~current_bit

			# zıt duvarı da kırma
			opposite_route = directions[ch_route]["opposite"]
			opposite_bit = directions[opposite_route]["bit"]
			maze_grid[ch_y][ch_x] &= ~opposite_bit

			visited[ch_y][ch_x] = True
			stack.append((ch_x, ch_y))
			current_x, current_y = ch_x, ch_y
		else:
			stack.pop()
			if stack:
				current_x, current_y = stack[-1]

	bfs(y, x, maze_grid, data)
	
def bfs(y, x, maze_grid, data):
	visited_lst = visited_list(y, x, maze_grid)
	finish_x, finish_y = map(int, data["EXIT"].split(','))
	queue = deque([(x, y)])
	parent = {(x, y): None}
	finded = False

	directions = {
			"North": (0, -1, 1),
			"East": (1, 0, 2),
			"South": (0, 1, 4),
			"West": (-1, 0, 8)
		}

	while queue:
		current_x, current_y = queue.popleft()

		if current_x == finish_x and current_y == finish_y:
			finded = True
			break
		cell_value = maze_grid[current_y][current_x]

		for route, (dx, dy, bit) in directions.items():
			new_x, new_y = current_x + dx, current_y + dy

			if 0 <= new_x < int(data["WIDTH"]) and 0 <= new_y < int(data["HEIGHT"]):
				if not visited_lst[new_y][new_x]:
					if (cell_value & bit) == 0:
						visited_lst[new_y][new_x] = True
						parent[(new_x, new_y)] = ((current_x, current_y), route[0].upper())
						queue.append((new_x, new_y))



	path_coords = set()
	path_letters = []
	if finded:
		curr = (finish_x, finish_y)
		while parent[curr] is not None:
			prev_cell, letter = parent[curr]
			path_letters.append(letter)
			curr = prev_cell
			path_coords.add(curr)
		path_letters.reverse()

	print_maze(maze_grid, path_coords)
	config_write(maze_grid, data, path_letters)
	
        
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
            
            # Eğer yol üzerindeyse ortaya nokta veya yıldız koyalım, değilse boşluk
            if (x, y) in path_coords:
                center = " * "
            else:
                center = "   "
                
            bottom = "___" if (cell & 4) else center
            right = "|" if (cell & 2) else " "
            line += bottom + right
        print(line)

if __name__ == "__main__":
	algorithm()
	