import os

def tema(index):
	COLORS = [
			'\033[94m', # Mavi
			'\033[92m', # Yeşil
			'\033[91m', # Kırmızı
			'\033[96m', # Turkuaz (Cyan)
			'\033[93m', # Sarı
			'\033[95m' # Mor
		]
	return COLORS[index]

def clear_screen():
	os.system('clear')

def print_maze1(grid, entry, finish, width, height, path_coords: list[tuple] | None = None, color: str | None = None):
	clear_screen()
	sifirla = '\033[0m'
	if not color:
		color = sifirla
	if not path_coords:
		path_coords = [()]

	üst_satir = color + "+"
	for _ in range(width):
		üst_satir += "---+"
	print(üst_satir)

	for y in range(height):
		orta_satir = "|"
		alt_satir = "+"
		for x in range(width):
			hücre = (x, y)
			if hücre == entry:
				orta_satir += sifirla + " E " + color
			elif hücre == finish:
				orta_satir += sifirla + " X " + color
			elif hücre in path_coords:
				orta_satir += sifirla + " * " + color
			elif grid[y][x] == 15:
				orta_satir += sifirla + "###" + color
			else:
				orta_satir += "   "
				
			# --- 2. ADIM: SAĞ DUVAR ---
			if grid[y][x] & 2:
				orta_satir += "|"
			else:
				orta_satir += " "
				
			# --- 3. ADIM: ALT DUVAR ---
			if grid[y][x] & 4:
				alt_satir += "---+"
			else:
				alt_satir += "   +"
		print(orta_satir)
		print(alt_satir)
	print(sifirla, end="")
