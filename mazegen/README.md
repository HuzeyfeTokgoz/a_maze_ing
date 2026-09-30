# mazegen

Bu paketi 42'nin A-Maze-ing projesi için yazdık ve sonraki projelerde
tekrar kullanabilmek için ayrı bir paket yaptık. Labirenti derinlik
öncelikli arama (DFS) ile oluşturuyor, istenirse içine döngüler ekliyor ve
girişten çıkışa en kısa yolu genişlik öncelikli arama (BFS) ile buluyor.

## Kurulum

```
pip install mazegen-1.0.0-py3-none-any.whl
```

## Temel örnek

```python
from mazegen import MazeGenerator

generator = MazeGenerator("config.txt")
generator.generate()        # labirenti üretir ve OUTPUT_FILE'a yazar

print(generator.solution)   # en kısa yol, örneğin "EESSWS..."
```

## Config dosyası

```python
MazeGenerator(path)
```

`path`, `KEY=VALUE` satırlarından oluşan bir config dosyası. `#` ile
başlayan satırları ve boş satırları atlıyoruz.

| Anahtar | Anlamı |
|---------|--------|
| `WIDTH`, `HEIGHT` | Hücre cinsinden labirent boyutu (1–50) |
| `ENTRY`, `EXIT` | `x,y` hücreleri; labirentin içinde ve birbirinden farklı |
| `OUTPUT_FILE` | `generate()` sonrası labirentin yazıldığı dosya |
| `PERFECT` | `True`: iki hücre arasında tam olarak bir yol. `False`: döngülü labirent, en az 5x5 |
| `SEED` | İsteğe bağlı. Aynı seed aynı labirentleri verir; yoksa rastgele |

Örnek `config.txt`:

```
# Default A-Maze-ing configuration
WIDTH=20
HEIGHT=15

ENTRY=0,0
EXIT=19,14
SEED=42

OUTPUT_FILE=maze.txt
PERFECT=False
```

Boyut, seed gibi parametreleri değiştirmek için bu dosyadaki değerleri
değiştirip dosyanın yolunu `MazeGenerator`'a vermeniz yeterli.

Dosya okunamazsa veya bir değerin biçimi yanlışsa `ConfigError`; giriş /
çıkış labirentin dışındaysa, aynı hücreyse, "42"nin üstündeyse veya
labirent döngüler için çok küçükse `ValueError` fırlatıyoruz.
`generate()` her çağrıldığında yeni bir labirent üretiyor ve
`OUTPUT_FILE`'ı yeniden yazıyor.

## Labirente ve çözüme erişim

- `generator.grid`: satırların listesi; `grid[y][x]`, `(x, y)`
  hücresi. Her hücre, bitleri kapalı duvarları gösteren bir tam sayı:
  Kuzey = 1, Doğu = 2, Güney = 4, Batı = 8 (15 = bütün duvarlar kapalı).
- `generator.solution`: `N`, `E`, `S`, `W` harflerinden oluşan en kısa yol.
- `generator.path_coords`: girişten çıkışa en kısa yolun hücreleri.
- `generator.pattern_cells`: "42"yi çizen kapalı hücreler (labirent
  "42" için çok küçükse boş).

## Çıktı dosyası

`generate()`, labirenti `OUTPUT_FILE`'a şu formatta yazıyor: her hücre tek
bir onaltılık rakam (duvar bitleri), labirentin her satırı dosyada ayrı
bir satır. Boş bir satırdan sonra giriş, çıkış ve en kısa yol geliyor.

## Dışa açılanlar

Paketten sadece `MazeGenerator` ve `ConfigError` import ediliyor:

```python
from mazegen import ConfigError, MazeGenerator
```
