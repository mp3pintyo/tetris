import pygame

# Initialize pygame before trying to use fonts
pygame.init()
pygame.font.init()  # Explicitly initialize the font module

# Játék alapbeállítások
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
PLAY_WIDTH = 300  # játéktér szélessége (10 blokk, egyenként 30 pixel)
PLAY_HEIGHT = 600  # játéktér magassága (20 blokk, egyenként 30 pixel)
BLOCK_SIZE = 30
PREVIEW_SIZE = 4 * BLOCK_SIZE
INITIAL_Y_OFFSET = -2  # Kezdő Y pozíció az elemeknek

# Játéktér pozíciója
TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = 60  # Módosítva fix értékre, hogy magasabban kezdődjön a játéktér

# Színek (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (200, 200, 200)
BG_COLOR_1 = (25, 25, 40)  # Sötét kék/lila háttér
BG_COLOR_2 = (45, 45, 80)  # Világosabb kék/lila átmenethez

# Modern színpaletta
MODERN_RED = (231, 76, 60)
MODERN_BLUE = (52, 152, 219)
MODERN_GREEN = (46, 204, 113)
MODERN_PURPLE = (155, 89, 182)
MODERN_ORANGE = (230, 126, 34)
MODERN_YELLOW = (241, 196, 15)
MODERN_CYAN = (26, 188, 156)

# Tetromino alakzatok (L, J, I, O, S, Z, T)
SHAPES = [
    [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],  # S
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']],
    
    [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],  # Z
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']],
    
    [['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],  # J
     ['.....',
      '.00..',
      '.0...',
      '.0...',
      '.....'],
     ['.....',
      '.....',
      '.0...',
      '.000.',
      '.....'],
     ['.....',
      '...0.',
      '...0.',
      '..00.',
      '.....']],
    
    [['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],  # L
     ['.....',
      '...0.',
      '...0.',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.0...',
      '.000.',
      '.....'],
     ['.....',
      '.00..',
      '.0...',
      '.0...',
      '.....']],  # Kijavított 4. rotáció
    
    [['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],  # T
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '..0..',
      '.000.',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....']],
    
    [['.....',
      '.....',
      '..00.',
      '..00.',
      '.....']],  # O
    
    [['.....',
      '.....',
      '.0000',
      '.....',
      '.....'],  # I
     ['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....']]
]

# Alakzatok színei (modern színpalettával)
SHAPE_COLORS = [
    MODERN_GREEN,   # S
    MODERN_RED,     # Z
    MODERN_BLUE,    # J
    MODERN_ORANGE,  # L
    MODERN_PURPLE,  # T
    MODERN_YELLOW,  # O
    MODERN_CYAN     # I
]

# Játékparaméterek
INITIAL_SPEED = 500  # kezdeti esési sebesség (ms)
MIN_SPEED = 100      # minimális esési sebesség (ms)
SPEED_FACTOR = 20    # gyorsulás mértéke szintenként
MOVE_REPEAT_DELAY = 100  # gombok ismétlési ideje (ms)

# Pontrendszer
SOFT_DROP_POINTS = 1    # pontok gyors ejtésért (le nyíl)
HARD_DROP_POINTS = 2    # pontok azonnali ejtésért (space)
SINGLE_LINE_POINTS = 100  # 1 sor kitörlése
DOUBLE_LINE_POINTS = 300  # 2 sor kitörlése
TRIPLE_LINE_POINTS = 500  # 3 sor kitörlése
TETRIS_POINTS = 800       # 4 sor kitörlése
COMBO_POINTS = 50         # combo bónusz pontonként

# Betűtípusok
try:
    # Initialize fonts after pygame is initialized
    FONT_LARGE = pygame.font.Font(None, 60)
    FONT_MEDIUM = pygame.font.Font(None, 36)
    FONT_SMALL = pygame.font.Font(None, 24)
except pygame.error:
    print("Warning: Failed to load system font, falling back to default")
    FONT_LARGE = pygame.font.SysFont('arial', 60)
    FONT_MEDIUM = pygame.font.SysFont('arial', 36)
    FONT_SMALL = pygame.font.SysFont('arial', 24)
except Exception as e:
    print(f"Warning: Font initialization failed: {e}")
    # Last resort - if all font initialization fails, create dummy font objects
    class DummyFont:
        def render(self, *args, **kwargs):
            return pygame.Surface((1, 1))
    FONT_LARGE = FONT_MEDIUM = FONT_SMALL = DummyFont()

# Hangfájlok útvonalai
SOUND_ROTATE = 'sounds/rotate.wav'
SOUND_CLEAR = 'sounds/clear.wav'
SOUND_FALL = 'sounds/fall.wav'
SOUND_GAME_OVER = 'sounds/gameover.wav'
SOUND_MOVE = 'sounds/move.wav'

# Hangerőbeállítások
VOLUME_ROTATE = 0.3
VOLUME_CLEAR = 0.5
VOLUME_FALL = 0.4
VOLUME_GAME_OVER = 0.6
VOLUME_MOVE = 0.2