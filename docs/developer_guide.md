# 🧩 FEJLESZTŐI ÚTMUTATÓ 🧩

![Developer Guide Banner](assets/dev_banner.png)

## 🏗️ ARCHITEKTÚRA ÁTTEKINTÉS

A **Modern Tetris** projekt egy moduláris szerkezetű, jól szervezett kódstruktúrán alapul, ami megkönnyíti a karbantartást és bővítést. Az alábbiakban részletesen bemutatjuk a projekt összetevőit és azok működését.

### 📦 MODUL STRUKTÚRA

```
Modern Tetris
├── main.py           # Fő indítófájl
├── game.py           # Játéklogika
├── piece.py          # Tetris elemek
├── ui.py             # Felhasználói felület
├── config.py         # Konfigurációs beállítások
├── sounds/           # Hangeffektek
└── docs/             # Dokumentáció
```

## 📄 MODULOK RÉSZLETES LEÍRÁSA

### 🎮 MAIN.PY

A játék belépési pontja, amely inicializálja és elindítja a fő játékciklust.

```python
from game import TetrisGame

def main():
    """
    Tetris játék indítása.
    A moduláris szerkezet lehetővé teszi a különböző komponensek
    elkülönített kezelését és könnyebb karbantartását.
    """
    game = TetrisGame()
    game.run()

if __name__ == "__main__":
    main()
```

### ⚙️ GAME.PY

A játék fő logikája itt található. Ez a modul felelős a játékállapot kezeléséért, az elemek mozgatásáért, ütközések ellenőrzéséért, pontszámításért és a felhasználói input feldolgozásáért.

#### Főbb osztályok és funkciók:

- **TetrisGame** - A fő játékosztály
- **reset_game()** - A játék alaphelyzetbe állítása
- **valid_move()** - Ellenőrzi, hogy egy lépés érvényes-e
- **lock_piece()** - Az elem rögzítése a játéktéren
- **clear_lines()** - A teljes sorok törlése és pontszám frissítése
- **hard_drop()** - Elem azonnali leejtése
- **handle_input()** - Felhasználói bemenet kezelése

### 🧩 PIECE.PY

A különböző Tetris elemek (tetromino) viselkedését irányító modul.

```python
class Piece:
    """
    A Tetris játék egy elemét reprezentáló osztály.
    Kezeli az elem tulajdonságait és mozgását.
    """
    def __init__(self, x, y, shape_index):
        # Elem inicializálása
        
    def get_shape(self):
        # Aktuális alakzat lekérése
        
    def rotate(self):
        # Elem forgatása
        
    def move_left/right/down(self):
        # Elem mozgatása
        
    def clone(self):
        # Elem másolása (pl. szellem elem létrehozásához)
```

### 🎨 UI.PY

A játék vizuális megjelenítéséért felelős modul, amely gondoskodik a grafikus elemek renderelésről.

#### Főbb funkciók:

- **draw_background()** - Animált háttér rajzolása
- **draw_grid_blocks()** - A játéktér blokkjainak megjelenítése
- **draw_piece()** - Tetris elem rajzolása
- **draw_ghost_piece()** - "Szellem" elem megjelenítése (előnézet)
- **draw_score()** - Pontszám és statisztikák kijelzése
- **draw_next_piece()** - Következő elem előnézete
- **draw_game_over()** / **draw_pause()** - Játék vége / szünet képernyők

### ⚙️ CONFIG.PY

Játék konfigurációs beállításait tartalmazó modul, amely centralizálja az összes konstans és paraméter kezelését.

```python
# Játék paraméterek
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
PLAY_WIDTH = 300
PLAY_HEIGHT = 600
BLOCK_SIZE = 30

# Tetromino alakzatok
SHAPES = [...]  # S, Z, J, L, T, O, I elemek definíciói

# Színpaletta
MODERN_RED = (231, 76, 60)
MODERN_BLUE = (52, 152, 219)
# ... további színek

# Játékmechanika beállítások
INITIAL_SPEED = 500  # Kezdeti esési sebesség (ms)
MIN_SPEED = 100      # Minimális esési sebesség (ms)
SPEED_FACTOR = 20    # Gyorsulás mértéke szintenként
```

## 🔄 JÁTÉK FOLYAMATA

### 🎲 INICIALIZÁLÁS

1. **main.py** inicializálja a **TetrisGame** osztályt
2. **TetrisGame** betölti a hangokat, inicializálja a grafikai felületet
3. A játék alapállapotba kerül: létrejönnek az első elemek, nullázódik a pontszám

### 🎯 FŐ JÁTÉKCIKLUS

```
     ┌─────────────────┐
     │  Játék indítása │
     └────────┬────────┘
              ▼
┌─────────────────────────┐
│  Felhasználói bemenet   │◄─────┐
│      feldolgozása       │      │
└────────────┬────────────┘      │
             ▼                   │
┌─────────────────────────┐      │
│   Játékállapot frissítése│      │
└────────────┬────────────┘      │
             ▼                   │
┌─────────────────────────┐      │
│      Képernyő rajzolás  │      │
└────────────┬────────────┘      │
             ▼                   │
┌─────────────────────────┐      │
│     Játék folytatódik?  │─Igen─┘
└────────────┬────────────┘
             │ Nem
             ▼
┌─────────────────────────┐
│     Játék befejezése    │
└─────────────────────────┘
```

## 🧪 TESZTELÉS

A Modern Tetris tesztelése manuálisan történik a következő fókuszterületeken:

1. **Játékmenet hibák** - Elemek megfelelő mozgatása, ütközésdetektálás, játék vége állapot
2. **Grafikai megjelenítés** - UI elemek elhelyezkedése, animációk
3. **Teljesítmény** - Képkockaszám stabilitása, memóriahasználat

## 🔧 BŐVÍTÉSI LEHETŐSÉGEK

A kód moduláris felépítése számos bővítési lehetőséget kínál:

### 👾 ÚJ JÁTÉKMÓDOK
- **Időzítős mód** - Adott idő alatt kell minél több pontot szerezni
- **Puzzle mód** - Előre meghatározott alakzatok kirakása
- **Több játékos mód** - Verseny másik játékos ellen

### 🎛️ TOVÁBBI TESTRESZABÁSI OPCIÓK
- **Egyedi témák** - Különböző vizuális stílusok
- **Egyedi kontrollok** - Billentyűzetbeállítások módosítása
- **Nehézségi szintek** - Kezdeti sebesség beállítása

### 🏆 RANGLISTÁK
- **Online pontszám megosztása**
- **Helyi játékos statisztikák**

## 🔍 HIBAELHÁRÍTÁS ÉS TIPPEK FEJLESZTŐKNEK

### 🐞 ISMERT HIBÁK KEZELÉSE

1. **Problémák az elemek forgatásával**
   - Ellenőrizd az alakzatdefiníciókat (SHAPES) a config.py-ban
   - Az alakzatok egyes rotációinak összefüggőnek kell lenniük

2. **Sorok törlésével kapcsolatos problémák**
   - A pozíciók frissítésének sorrendje kritikus a clear_lines() függvényben

3. **UI elemek átlapolódása**
   - Az elemek pozícionálását a config.py-ban és az ui.py-ban kell beállítani

### 💻 FEJLESZTÉSI TIPPEK

1. **Új elem hozzáadása**
   ```python
   # Új elem hozzáadása a SHAPES tömbhöz a config.py-ban
   [['.....',
     '.....',
     '..00.',
     '..00.',
     '..00.'],
     ... további rotációk]
   ```

2. **Új funkció implementálása**
   - Használd a meglévő osztályszerkezetet
   - Bontsd a feladatot logikai egységekre
   - Tartsd szem előtt a modularitást

---

<p align="center">
  <strong>🚀 MODERN TETRIS - FEJLESZTŐI DOKUMENTÁCIÓ 🚀</strong><br>
  <em>Készítette a GitHub Copilot csapat | © 2025</em>
</p>