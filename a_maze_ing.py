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

if __name__ == "__main__":
	data = config_read()
	for _ in range(int(data["WIDTH"])):
		for _ in range(int(data["HEIGHT"])):
			seed_val = data.get("SEED", 42)
			lab = random.seed(seed_val)
			print(lab, end=" ")
		print()

# kenarlar
# komşularının durumları
config_read()