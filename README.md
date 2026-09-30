*This project has been created as part of the 42 curriculum by hutokgoz, mburdurl.*

# A-Maze-ing

## Açıklama

A-Maze-ing, Python ile yazdığımız bir labirent üreticisi. Program bir
config dosyasını okuyor, rastgele (ama seed ile tekrar üretilebilen) bir
labirent oluşturuyor, bunu onaltılık (hex) formatta bir dosyaya yazıyor ve
terminalde gösteriyor.

İki tür labirent üretebiliyoruz:

- **Mükemmel labirent** (`PERFECT=True`): herhangi iki hücre arasında tam
  olarak bir yol var.
- **Pac-Man tahtası** (`PERFECT=False`, konudaki varsayılan mod): bütün
  koridorlara ulaşılabiliyor, tahtada birden fazla döngü var ve hiç çıkmaz
  sokak yok. Böylece hayaletlerden kaçan oyuncunun her zaman başka bir
  yolu oluyor.

Labirent yeterince büyükse içine tamamen kapalı hücrelerden bir "42"
çiziyoruz.

Labirent üretme kodunu ayrı bir paket olan `mazegen` içine koyduk; pip ile
kurulup başka bir projede tekrar kullanılabiliyor.

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

`make install`, projede kullandığımız araçları kuruyor: `flake8`, `mypy`
ve `build`.

### Çalıştırma

```
make run
```

ya da

```
python3 a_maze_ing.py <config_dosyası>
```

`make run`, repo'daki `config.txt` dosyasını kullanıyor. Labirent
`OUTPUT_FILE` ile verilen dosyaya yazılıyor ve terminalde şu menüyle
gösteriliyor:

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
`dist/mazegen-1.0.0.tar.gz` dosyalarını üretiyor. Build ettiğimiz wheel
dosyasını repo'nun kök klasörüne de koyduk.

## Config dosyası

Her satırda bir `KEY=VALUE` çifti var. Boş satırları ve `#` ile
başlayan satırları yok sayıyoruz.

| Anahtar | Zorunlu | Açıklama | Örnek |
|---------|---------|----------|-------|
| `WIDTH` | evet | Hücre cinsinden genişlik, 1 ile 50 arası | `WIDTH=20` |
| `HEIGHT` | evet | Hücre cinsinden yükseklik, 1 ile 50 arası | `HEIGHT=15` |
| `ENTRY` | evet | Giriş hücresi `x,y` | `ENTRY=0,0` |
| `EXIT` | evet | Çıkış hücresi `x,y` | `EXIT=19,14` |
| `OUTPUT_FILE` | evet | Labirentin yazılacağı dosya | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | evet | `True` veya `False` (büyük/küçük harf fark etmez) | `PERFECT=False` |
| `SEED` | hayır | Tam sayı; aynı seed aynı labirenti verir | `SEED=42` |

Program şu durumlarda çökmeden, anlaşılır bir hata mesajıyla duruyor:

- dosya okunamazsa, bir satırda `=` yoksa, bir anahtar boşsa, iki kez
  yazılmışsa, bilinmiyorsa ya da zorunlu bir anahtar eksikse;
- bir değerin tipi veya formatı yanlışsa, ya da boyut izin verilen
  aralığın dışındaysa;
- `ENTRY` veya `EXIT` labirentin dışındaysa, "42"nin içindeyse ya da ikisi
  aynı hücreyse;
- `OUTPUT_FILE` boşsa ya da config dosyasının kendisiyse;
- `PERFECT=False`, 5x5'ten küçük bir labirentte kullanılırsa (döngü
  oluşturmak için çok küçük).

Labirent 9x7'den küçükse "42" sığmıyor: bu durumda deseni atlıyoruz ve bir
uyarı gösteriyoruz.

Repo'daki varsayılan `config.txt`:

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

Her hücreyi tek bir onaltılık rakam olarak yazıyoruz. Rakamın bitleri
kapalı duvarları gösteriyor: Kuzey = 1, Doğu = 2, Güney = 4, Batı = 8.
Labirentin her satırı dosyada ayrı bir satır. Boş bir satırdan sonra
giriş, çıkış ve `N`, `E`, `S`, `W` harfleriyle en kısa yol geliyor.

## Labirent üretme algoritması

1. **Derinlik öncelikli arama (DFS, recursive backtracker).** Başta bütün
   duvarlar kapalı. Girişten başlayıp rastgele, henüz ziyaret edilmemiş
   bir komşuya geçiyoruz ve aradaki duvarı açıyoruz. Gidecek yer
   kalmayınca bir yığın (stack) ile geri dönüyoruz. "42"nin hücrelerini
   baştan ziyaret edilmiş sayıyoruz, böylece kapalı kalıyorlar. Sonuç
   mükemmel bir labirent oluyor.
2. **Çıkmaz sokakları açma (braiding)**, sadece `PERFECT=False` ile. Her
   çıkmaz sokakta (3 duvarı kapalı hücre) "42"ye ait olmayan rastgele bir
   komşuya doğru bir duvar daha açıyoruz. Bu hem döngüler oluşturuyor hem
   de çıkmaz sokakları kaldırıyor.
3. **Genişlik öncelikli arama (BFS).** Girişten çıkışa en kısa yolu BFS
   ile buluyoruz. Her adımın maliyeti aynı olan bir ızgarada BFS en kısa
   yolu garanti ediyor.

### Bu algoritmayı neden seçtik

- Anlaması ve adım adım anlatması kolay.
- Her zaman mükemmel bir labirent üretiyor; `PERFECT=True`'nun istediği
  tam olarak bu. Pac-Man tahtasını da bunun üzerine küçük bir ek adımla
  elde edebiliyoruz.
- Uzun ve dolambaçlı koridorlar üretiyor; hem iyi görünüyor hem de
  ilginç yollar çıkıyor.
- Özyineleme (recursion) yerine kendi yığınımızı kullandığımız için büyük
  labirentlerde Python'un özyineleme sınırına takılmıyoruz.
- Bütün çıkmaz sokakları açınca hiç çıkmaz sokağı olmayan bir tahta
  çıkıyor; bu da konunun bonus kısmı.

## Tekrar kullanılabilir kod: `mazegen` paketi

Labirent üretmek için gereken her şeyi `mazegen/` klasörüne koyduk. Paket
pip ile kurulabiliyor:

```
pip install mazegen-1.0.0-py3-none-any.whl
```

Ekran çizimi (`print_maze.py`, `themes.py`) ve menü (`a_maze_ing.py`)
bilerek paketin dışında; paketi kullanan bir proje kendi ekranını
yazabilsin istedik.

### Temel örnek

```python
from mazegen import MazeGenerator

generator = MazeGenerator("config.txt")
generator.generate()        # labirenti üretir ve OUTPUT_FILE'a yazar
print(generator.solution)   # en kısa yol, örneğin "EESSWS..."
```

### Parametreler

```python
MazeGenerator(path)
```

- `path`: config dosyasının yolu. `WIDTH`, `HEIGHT`, `ENTRY`, `EXIT`,
  `OUTPUT_FILE`, `PERFECT` ve isteğe bağlı `SEED` buradan okunuyor
  (biçimi ve örnek dosya için yukarıdaki "Config dosyası" bölümüne
  bakın).

Boyut, seed gibi özel parametreleri config dosyasındaki değerleri
değiştirerek veriyoruz.

Geçersiz bir config `ConfigError`, geçersiz giriş / çıkış veya döngüler
için çok küçük bir labirent `ValueError` fırlatıyor. `generate()` her
çağrıldığında yeni bir labirent üretiyor ve `OUTPUT_FILE`'ı yeniden
yazıyor.

### Labirente ve çözüme erişim

- `generator.grid`: `grid[y][x]`, `(x, y)` hücresinin duvar bitleri
  (Kuzey = 1, Doğu = 2, Güney = 4, Batı = 8).
- `generator.solution`: `N`, `E`, `S`, `W` harfleriyle en kısa yol.
- `generator.path_coords`: girişten çıkışa en kısa yolun hücreleri.
- `generator.pattern_cells`: "42"yi çizen kapalı hücreler.

Paket ayrıca config dosyasını tek başına okumak için `parse_config()` ve
çıktı dosyasını yazmak için `write_output()` sağlıyor. Paketin kendi
belgesi `mazegen/README.md` dosyasında.

### Kontrolleri nasıl ayırdık

- `parser.py` her değerin **biçimini** kontrol ediyor: anahtarlar, tipler,
  `x,y` formatı, 1–50 boyut aralığı, `OUTPUT_FILE`. Hataları `ConfigError`
  olarak fırlatıyor.
- `generator.py` değerlerin **labirent için anlamlı** olup olmadığını
  kontrol ediyor: giriş / çıkış labirentin içinde mi, farklı hücreler mi,
  "42"nin üstünde mi, `PERFECT=False` için labirent yeterince büyük mü.
  Hataları `ValueError` olarak fırlatıyor. Bu kurallar generator'ın kendi
  sabitlerine (`MIN_LOOP_SIZE`, `PATTERN_42`) bağlı olduğu için onları
  orada bıraktık.

## Ek özellikler

- **Renk temaları**: altı tema (Classic, Ocean, Forest, Lava, Neon, Sand)
  ekledik. Her tema duvarları, "42"yi, yolu ve giriş / çıkış işaretlerini
  ayrı ayrı renklendiriyor. Temalar `themes.py` içinde.
- **Hiç çıkmaz sokak olmaması** (bonus), Pac-Man modunda: bunu konuyla
  birlikte verilen analiz script'iyle kontrol ettik
  (`maze_analyzer.py --max-dead-ends 0`).

## Takım ve proje yönetimi

### Takım ve roller

Projeyi iki kişi yaptık:

- **hutokgoz**: labirent üretimi ve `mazegen` paketi. DFS ile labirent
  oluşturma, `PERFECT=False` için döngü ekleme (braiding), BFS ile en
  kısa yol, "42" deseni, `MazeGenerator` sınıfı, `pyproject.toml` ve 
  menü (`a_maze_ing.py`).
- **mburdurl**: programın kullanıcıya bakan tarafı. Config dosyasını
  okuma ve kontrol etme (`parser.py`, `error.py`), çıktı dosyası
  (`writer.py`), terminalde çizim (`print_maze.py`), renk temaları
  (`themes.py`).

Makefile, lint ayarları, README ve testleri birlikte yaptık.

### Planlama

Planımız önce çalışan bir çekirdek kurup sonra üzerine katman eklemekti.
İşi iki paralel koldan yürüttük: biri labirent algoritmaları, diğeri
config okuma ve ekran. İki taraf `grid` yapısı (her hücre bir duvar
bitmask'i) üzerinde baştan anlaştığı için birbirini beklemeden
ilerleyebildi.

Gerçekte ilerleyiş şöyle oldu:

1. ızgara yapısı, DFS ile labirent üretimi ve BFS ile en kısa yol;
2. "42" deseninin labirente yerleştirilmesi;
3. kodun `MazeGenerator` sınıfında toplanması ve `PERFECT=False` için
   döngü ekleme;
4. terminalde çizim, menü ve renk temaları;
5. config kontrolleri, hata sınıfı ve çıktı dosyası;
6. `pyproject.toml`, wheel, Makefile, lisans ve README;
7. son olarak generator'ın config dosyasını kendisinin okuması ve çıktı
   dosyasını `generate()` içinde yazması.

Config okumayı ve paketlemeyi sona bırakmıştık; bu yüzden en sonda
generator'ın arayüzünü değiştirmemiz ve wheel'i yeniden build etmemiz
gerekti.

### İyi giden şeyler

- İşi algoritma ve ekran olarak ikiye bölmek, ikimizin aynı anda
  çalışmasını sağladı; çizim hatalarını labirent hatalarından ayırmak da
  kolaylaştı.
- `flake8` ve `mypy --strict`'i erken kullanmaya başladığımız için tip
  hatalarını büyümeden yakaladık.

### Araçlar

Git ve GitHub, VS Code, virtualenv, flake8, mypy, setuptools / build.

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

Yapay zekâyı (Claude) şu işlerde yardımcı olarak kullandık:

- kodu konuyla karşılaştırıp incelemek ve hataları bulmak (menü durumu,
  Ctrl-D ile çökme, config dosyasının üzerine yazılması, yeterince
  döngüsü olmayan küçük Pac-Man labirentleri);
- renk teması tasarımı, Makefile, lint ayarları ve `pyproject.toml` için
  öneriler;
- generator'ı config dosyasını okuyacak şekilde değiştirdikten sonra
  etkilenen yerleri (`a_maze_ing.py`, docstring'ler, README'ler, wheel)
  bulup güncellemek ve `write_output`'u `generate()` içine almak;
- docstring'lerin ve README'nin taslağını yazmak.

Her öneriyi kullanmadan önce inceledik, test ettik ve kendi kodumuza
uyarladık. Labirent üretimini, çözücüyü ve genel tasarımı kendimiz yazdık.
