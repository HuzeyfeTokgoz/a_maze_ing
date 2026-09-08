# 1111
import random
# 0011
# 8421
a = 16

def config_read():
	try:
		data = {}
		with open("config.txt") as dosya:
			for line in dosya:
				if not line or line.startswith('#'):
					continue
				if "=" in line:
					key, value = line.split("=", 1)
					data[key] = value
	except Exception:
		print("Dosya bulunamadı")
		return None
	else:
		return data

def maze():
	data = config_read()
	seed_val = data.get("SEED", 42)
	random.seed(seed_val)
	
	maze_grid = []
	for _ in range(int(data["WIDTH"])):
		row = []
		for _ in range(int(data["HEIGHT"])):
			row.append(15)
		maze_grid.append(row)
	return maze_grid

def algoritma():
	data = config_read()
	maze_grid = maze()
	x, y = map(int, data["ENTRY"].split(','))
	current_x, current_y = x, y
	coor = {
		"North": (x, y - 1),
		"South": (x, y + 1),
		"East": (x + 1, y),
    	"West":  (x - 1, y)
		}

	finish_x, finish_y = map(int, data["EXIT"].split(','))

# ziyaret listesi
	stack = []
	visited = []
	for i in maze_grid:
		row = []
		for _ in i:
			row.append(False)
		visited.append(row)

	visited[current_y][current_x] = True
	stack.append((current_x, current_y))
	print(visited)
	print(stack)



if __name__ == "__main__":
	algoritma()
# kenarlar
# komşularının durumları