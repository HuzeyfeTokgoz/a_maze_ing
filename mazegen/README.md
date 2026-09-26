# mazegen

A-Maze-ing projesinden çıkan, tekrar kullanılabilir labirent üreticisi.
Labirenti derinlik öncelikli arama (DFS) ile oluşturur, isteğe bağlı olarak
içine döngüler ekler ve girişten çıkışa en kısa yolu genişlik öncelikli
arama (BFS) ile bulur.

## Kurulum

```
pip install mazegen-1.0.0-py3-none-any.whl
```

## Temel örnek

```python
from mazegen import MazeGenerator

generator = MazeGenerator(20, 15, (0, 0), (19, 14))
generator.generate()

print(generator.solution)   # en kısa yol, örneğin "EESSWS..."
```

## Parametreler

```python
MazeGenerator(width, height, entry, exit, perfect=False, seed=None)
```

| Parametre | Anlamı |
|-----------|--------|
| `width`, `height` | Hücre cinsinden labirent boyutu |
| `entry`, `exit` | `(x, y)` hücreleri; labirentin içinde ve birbirinden farklı |
| `perfect` | `True`: iki hücre arasında tam olarak bir yol. `False` (varsayılan): döngülü labirent, en az 5x5 |
| `seed` | Aynı seed aynı labirentleri verir. `None` rastgele bir labirent verir |

Geçersiz parametreler `ValueError` fırlatır.
`generate()` tekrar çağrıldığında yeni bir labirent üretir.

## Labirente ve çözüme erişim

- `generator.grid`: satırların listesi; `grid[y][x]`, `(x, y)`
  hücresidir. Her hücre, bitleri kapalı duvarları gösteren bir tam
  sayıdır: Kuzey = 1, Doğu = 2, Güney = 4, Batı = 8 (15 = bütün duvarlar
  kapalı).
- `generator.solution`: `N`, `E`, `S`, `W` harflerinden oluşan en kısa yol.
- `generator.path_coords`: girişten çıkışa en kısa yolun hücreleri.
- `generator.pattern_cells`: "42"yi çizen kapalı hücreler (labirent
  "42" için çok küçükse boş).

## Config dosyası ve çıktı dosyası (isteğe bağlı)

```python
from mazegen import ConfigError, MazeGenerator, parse_config, write_output

config = parse_config("config.txt")      # geçersizse ConfigError fırlatır
generator = MazeGenerator(config.width, config.height, config.entry,
                          config.exit, config.perfect, config.seed)
generator.generate()
write_output(config.output_file, generator.grid, generator.entry,
             generator.exit, generator.solution)
```
