*This project has been created as part of the 42 curriculum by hutokgoz.*

# A-Maze-ing

## Açıklama

A-Maze-ing, Python ile yazılmış bir labirent üreticisidir.
Bir config dosyasını okur, rastgele (ama tekrar üretilebilir) bir labirent
oluşturur, labirenti onaltılık (hex) formatta bir dosyaya yazar ve
terminalde gösterir.

İki tür labirent üretilebilir:

- **Mükemmel labirent** (`PERFECT=True`): herhangi iki hücre arasında tam
  olarak bir yol vardır.
- **Pac-Man tahtası** (`PERFECT=False`, varsayılan): bütün koridorlara
  ulaşılabilir, tahtada birden fazla döngü vardır ve hiç çıkmaz sokak
  yoktur. Böylece hayaletlerden kaçan oyuncunun her zaman başka bir yolu
  olur.

Labirent yeterince büyükse içinde tamamen kapalı hücrelerle çizilmiş bir
"42" bulunur.

Labirent üretme kodu ayrı bir paket olan `mazegen` içindedir; pip ile
kurulup başka bir projede tekrar kullanılabilir.

## Kullanım talimatları

### Gereksinimler

- Python 3.10 veya üstü
- ANSI renklerini destekleyen bir terminal

### Kurulum

```
python3 -m venv a_maze
source a_maze/bin/activate
make install
```

`make install`, projede kullanılan araçları kurar: `flake8`, `mypy` ve
`build`.

### Çalıştırma

```
python3 a_maze_ing.py config.txt
```

ya da kısaca `make run`. Labirent `OUTPUT_FILE` ile verilen dosyaya yazılır
ve terminalde şu menüyle gösterilir:

| Tuş | İşlem |
|-----|-------|
| `1` | Yeni labirent üret (çıktı dosyası da güncellenir) |
| `2` | En kısa yolu göster / gizle |
| `3` | Renk temasını değiştir |
| `4` | Çıkış |

### Makefile kuralları

| Kural | Açıklama |
|-------|----------|
| `make install` | Geliştirme araçlarını kurar |
| `make run` | Programı `config.txt` ile çalıştırır |
| `make debug` | Programı `pdb` hata ayıklayıcısıyla çalıştırır |
| `make clean` | Önbellek ve build dosyalarını siler |
| `make lint` | `flake8` ve `mypy`'yi konudaki parametrelerle çalıştırır |
| `make lint-strict` | `flake8` ve `mypy --strict` çalıştırır |

### `mazegen` paketini build etmek

```
python3 -m build
```

Bu komut `dist/mazegen-1.0.0-py3-none-any.whl` ve
`dist/mazegen-1.0.0.tar.gz` dosyalarını üretir. Build edilmiş wheel
dosyası repo'nun kök klasöründe de bulunur.

## Config dosyası

Her satırda bir `ANAHTAR=DEĞER` çifti bulunur. Boş satırlar ve `#` ile
başlayan satırlar yok sayılır.

| Anahtar | Zorunlu | Açıklama | Örnek |
|---------|---------|----------|-------|
| `WIDTH` | evet | Hücre cinsinden genişlik, 1 ile 50 arası | `WIDTH=20` |
| `HEIGHT` | evet | Hücre cinsinden yükseklik, 1 ile 50 arası | `HEIGHT=15` |
| `ENTRY` | evet | Giriş hücresi `x,y` | `ENTRY=0,0` |
| `EXIT` | evet | Çıkış hücresi `x,y` | `EXIT=19,14` |
| `OUTPUT_FILE` | evet | Labirentin yazılacağı dosya | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | evet | `True` veya `False` (büyük/küçük harf fark etmez) | `PERFECT=False` |
| `SEED` | hayır | Tam sayı; aynı seed aynı labirenti verir | `SEED=42` |

Program şu durumlarda anlaşılır bir hata mesajıyla durur:

- dosya okunamazsa, bir satırda `=` yoksa, bir anahtar boşsa, iki kez
  yazılmışsa, bilinmiyorsa ya da zorunlu bir anahtar eksikse;
- bir değerin tipi veya formatı yanlışsa, ya da boyut izin verilen
  aralığın dışındaysa;
- `ENTRY` veya `EXIT` labirentin dışındaysa, "42"nin içindeyse ya da ikisi
  aynı hücreyse;
- `OUTPUT_FILE` boşsa ya da config dosyasının kendisiyse;
- `PERFECT=False`, 5x5'ten küçük bir labirentte kullanılırsa (döngü
  oluşturmak için çok küçük).

Labirent 9x7'den küçükse "42" sığmaz: atlanır ve bir uyarı gösterilir.

Varsayılan `config.txt`:

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

## Çıktı dosyası

Her hücre tek bir onaltılık rakam olarak yazılır. Rakamın bitleri kapalı
duvarları gösterir: Kuzey = 1, Doğu = 2, Güney = 4, Batı = 8. Her satır
ayrı bir satıra yazılır. Boş bir satırdan sonra giriş, çıkış ve `N`, `E`,
`S`, `W` harfleriyle en kısa yol gelir.

## Labirent üretme algoritması

1. **Derinlik öncelikli arama (DFS, recursive backtracker).** Başta bütün
   duvarlar kapalıdır. Algoritma girişten başlayarak rastgele, henüz
   ziyaret edilmemiş bir komşuya geçer ve aradaki duvarı açar. Gidecek
   yer kalmayınca bir yığın (stack) ile geri döner. "42"nin hücreleri
   başlamadan önce ziyaret edilmiş sayılır, böylece kapalı kalırlar.
   Sonuç mükemmel bir labirenttir.
2. **Çıkmaz sokakları açma (braiding)**, sadece `PERFECT=False` ile. Her
   çıkmaz sokakta (3 duvarı kapalı hücre) "42"ye ait olmayan rastgele bir
   komşuya doğru bir duvar daha açılır. Bu, döngüler oluşturur ve çıkmaz
   sokakları kaldırır.
3. **Genişlik öncelikli arama (BFS).** Girişten çıkışa en kısa yol BFS ile
   bulunur. Her adımın maliyeti aynı olan bir ızgarada BFS en kısa yolu
   verir.

### Bu algoritmayı neden seçtik

- Anlaşılması ve adım adım anlatılması kolay.
- Her zaman mükemmel bir labirent üretir; bu tam olarak `PERFECT=True`'nun
  istediği şey. Pac-Man tahtası da bunun üzerine küçük bir ek adımla
  oluşturuluyor.
- Uzun ve dolambaçlı koridorlar üretir; bu hem iyi görünür hem de ilginç
  yollar oluşturur.
- Özyineleme (recursion) yerine kendi yığınımızı kullanmak, büyük
  labirentlerde Python'un özyineleme sınırına takılmayı önler.
- Bütün çıkmaz sokakları açmak hiç çıkmaz sokağı olmayan bir tahta verir;
  bu da konunun bonus kısmı.

## Tekrar kullanılabilir kod: `mazegen` paketi

Labirent üretmek için gereken her şey `mazegen/` klasöründedir ve pip ile
kurulabilir:

```
pip install mazegen-1.0.0-py3-none-any.whl
```

Ekran çizimi (`print_maze.py`, `themes.py`) ve menü (`a_maze_ing.py`)
paketin parçası değildir.

### Temel örnek

```python
from mazegen import MazeGenerator

generator = MazeGenerator(20, 15, (0, 0), (19, 14))
generator.generate()
print(generator.solution)   # en kısa yol, örneğin "EESSWS..."
```

### Parametreler

```python
MazeGenerator(width, height, entry, exit, perfect=False, seed=None)
```

- `width`, `height`: hücre cinsinden labirent boyutu.
- `entry`, `exit`: `(x, y)` hücreleri; labirentin içinde ve birbirinden
  farklı olmalı.
- `perfect`: mükemmel labirent için `True`, döngülü labirent için `False`
  (varsayılan, en az 5x5).
- `seed`: aynı seed aynı labirentleri verir; `None` rastgele bir labirent
  verir.

Geçersiz parametreler `ValueError` fırlatır. `generate()` tekrar
çağrıldığında yeni bir labirent üretir.

### Labirente ve çözüme erişim

- `generator.grid`: `grid[y][x]`, `(x, y)` hücresinin duvar bitleridir
  (Kuzey = 1, Doğu = 2, Güney = 4, Batı = 8).
- `generator.solution`: `N`, `E`, `S`, `W` harfleriyle en kısa yol.
- `generator.path_coords`: girişten çıkışa en kısa yolun hücreleri.
- `generator.pattern_cells`: "42"yi çizen kapalı hücreler.

Paket ayrıca config dosyası okumak için `parse_config()` (hata durumunda
`ConfigError` fırlatır) ve çıktı dosyasını yazmak için `write_output()`
sağlar. Aynı belge paketin içinde de bulunur (`mazegen/README.md`).

## Ek özellikler

- **Renk temaları**: altı tema (Classic, Ocean, Forest, Lava, Neon, Sand)
  duvarları, "42"yi, yolu ve giriş / çıkış işaretlerini ayrı ayrı
  renklendirir. Temalar `themes.py` içinde tanımlıdır.
- **Hiç çıkmaz sokak olmaması** (bonus), Pac-Man modunda: konuyla birlikte
  verilen analiz script'iyle kontrol edildi
  (`maze_analyzer.py --max-dead-ends 0`).

## Takım ve proje yönetimi

> TODO: bu bölümü doldur.

- **Takım ve roller**: TODO (kim ne yaptı).
- **Planlama**: TODO (başlangıçtaki plan ve sona kadar nasıl değişti).
- **İyi giden şeyler**: TODO
- **Daha iyi olabilecek şeyler**: TODO
- **Araçlar**: Git ve GitHub, VS Code, virtualenv, flake8, mypy, build.
  TODO: kullandığın başka araç varsa ekle.

## Kaynaklar

- [Maze generation algorithm (Wikipedia)](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Maze generation: recursive backtracking, Jamis Buck](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking)
- [Think Labyrinth: labirent algoritmaları ve braid labirentler](https://www.astrolog.org/labyrnth/algrithm.htm)
- [Breadth-first search (Wikipedia)](https://en.wikipedia.org/wiki/Breadth-first_search)
- [ANSI escape codes (Wikipedia)](https://en.wikipedia.org/wiki/ANSI_escape_code)
- [Python Packaging User Guide: packaging projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [PEP 8](https://peps.python.org/pep-0008/) ve
  [PEP 257](https://peps.python.org/pep-0257/)
- [mypy belgeleri](https://mypy.readthedocs.io/)

### Yapay zekâ kullanımı

> TODO: bu bölümü kontrol et ve yaptıklarına uyacak şekilde tamamla.

Yapay zekâ (Claude) şu işlerde yardımcı olarak kullanıldı:

- kodu konuyla karşılaştırıp incelemek ve hataları bulmak (menü durumu,
  Ctrl-D ile çökme, config dosyasının üzerine yazılması, yeterince
  döngüsü olmayan küçük Pac-Man labirentleri);
- renk teması tasarımı, Makefile, lint ayarları ve `pyproject.toml` için
  öneriler;
- docstring'lerin ve bu README'nin ilk taslağının yazılması.

Her öneri kullanılmadan önce incelendi, test edildi ve uyarlandı.
Labirent üretimi, çözücü ve genel tasarım takım tarafından yazıldı.
