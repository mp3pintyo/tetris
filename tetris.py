import pygame
import random
import time
from pygame import mixer
import math

# Initialize Pygame
pygame.init()
mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
PLAY_WIDTH = 300  # play area width (10 blocks of 30 pixels)
PLAY_HEIGHT = 600  # play area height (20 blocks of 30 pixels)
BLOCK_SIZE = 30
PREVIEW_SIZE = 4 * BLOCK_SIZE

# Calculate top-left position of play area to center it on screen
TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = SCREEN_HEIGHT - PLAY_HEIGHT - 50

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (200, 200, 200)
BG_COLOR_1 = (25, 25, 40)  # Dark blue/purple background
BG_COLOR_2 = (45, 45, 80)  # Lighter blue/purple for gradient

# Modern color palette
MODERN_RED = (231, 76, 60)
MODERN_BLUE = (52, 152, 219)
MODERN_GREEN = (46, 204, 113)
MODERN_PURPLE = (155, 89, 182)
MODERN_ORANGE = (230, 126, 34)
MODERN_YELLOW = (241, 196, 15)
MODERN_CYAN = (26, 188, 156)

# Tetromino shapes (L, J, I, O, S, Z, T)
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
      '...0.',
      '...0.',
      '.....']],
    
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

# Shape colors (using modern color palette)
SHAPE_COLORS = [
    MODERN_GREEN,   # S
    MODERN_RED,     # Z
    MODERN_BLUE,    # J
    MODERN_ORANGE,  # L
    MODERN_PURPLE,  # T
    MODERN_YELLOW,  # O
    MODERN_CYAN     # I
]

# Load fonts - using better looking fonts for a modern UI
try:
    # Try to load better fonts if available
    FONT_LARGE = pygame.font.Font(None, 60)
    FONT_MEDIUM = pygame.font.Font(None, 36)
    FONT_SMALL = pygame.font.Font(None, 24)
except:
    # Fallback to system fonts
    FONT_LARGE = pygame.font.SysFont('arial', 60)
    FONT_MEDIUM = pygame.font.SysFont('arial', 36)
    FONT_SMALL = pygame.font.SysFont('arial', 24)

class Piece:
    def __init__(self, x, y, shape_index):
        self.x = x
        self.y = y
        self.shape_index = shape_index
        self.color = SHAPE_COLORS[shape_index]
        self.rotation = 0
        self.shape = SHAPES[shape_index]

    def get_shape(self):
        return self.shape[self.rotation % len(self.shape)]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Modern Tetris - Készítette: GitHub Copilot')
        self.clock = pygame.time.Clock()
        self.reset_game()
        
        # Load sounds
        try:
            self.rotate_sound = mixer.Sound('rotate.wav')
            self.clear_sound = mixer.Sound('clear.wav')
            self.fall_sound = mixer.Sound('fall.wav')
            self.game_over_sound = mixer.Sound('gameover.wav')
            self.move_sound = mixer.Sound('move.wav')
            # Set volume
            self.rotate_sound.set_volume(0.3)
            self.clear_sound.set_volume(0.5)
            self.fall_sound.set_volume(0.4)
            self.game_over_sound.set_volume(0.6)
            self.move_sound.set_volume(0.2)
        except:
            # If sounds can't be loaded, create dummy functions
            self.rotate_sound = self.move_sound = self.clear_sound = self.fall_sound = self.game_over_sound = type('obj', (object,), {
                'play': lambda: None
            })
            print("Nem sikerült a hangfájlokat betölteni. Folytatás hang nélkül.")
        
        # UI animation variables
        self.animation_time = 0
        self.score_flash = 0
        
        # Create UI panel background surfaces
        self.create_ui_panels()
    
    def create_ui_panels(self):
        # Create reusable UI panel surfaces with rounded corners and gradients
        self.panel_main = self.create_panel(PLAY_WIDTH + 40, PLAY_HEIGHT + 40, 10)
        self.panel_next = self.create_panel(PREVIEW_SIZE * 2 + 40, PREVIEW_SIZE * 2 + 40, 5)
        self.panel_score = self.create_panel(200, 80, 5)
        self.panel_controls = self.create_panel(200, 220, 5)
        
    def create_panel(self, width, height, border_radius):
        # Create a panel surface with rounded corners and gradient
        panel = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Draw gradient background
        for y in range(height):
            # Calculate gradient color
            gradient_factor = y / height
            r = int(DARK_GRAY[0] * (1 - gradient_factor) + BG_COLOR_1[0] * gradient_factor)
            g = int(DARK_GRAY[1] * (1 - gradient_factor) + BG_COLOR_1[1] * gradient_factor)
            b = int(DARK_GRAY[2] * (1 - gradient_factor) + BG_COLOR_1[2] * gradient_factor)
            color = (r, g, b, 180)  # Semi-transparent
            
            # Draw horizontal line of the gradient
            pygame.draw.line(panel, color, (0, y), (width, y))
        
        # Draw rounded rectangle border
        pygame.draw.rect(panel, WHITE, (0, 0, width, height), 2, border_radius)
        
        return panel

    def reset_game(self):
        self.locked_positions = {}
        self.grid = self.create_grid()
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()
        self.change_piece = False
        self.game_over = False
        self.paused = False
        
        # Game stats
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.last_score_increase = 0
        self.combo = 0
        
        # Game speed (milliseconds per drop)
        self.drop_speed = 500
        self.last_drop_time = time.time() * 1000
        
        # Controls
        self.down_pressed = False
        self.move_repeat_delay = 100  # milliseconds
        self.last_move_time = {
            pygame.K_LEFT: 0,
            pygame.K_RIGHT: 0,
            pygame.K_DOWN: 0
        }

    def create_grid(self):
        # Create empty grid (20x10)
        return [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    def update_grid(self):
        # First create empty grid
        self.grid = self.create_grid()
        
        # Add locked pieces
        for (j, i), color in self.locked_positions.items():
            if i < 20:  # Check if within grid height
                self.grid[i][j] = color

    def get_new_piece(self):
        # Creates a new random piece
        piece = Piece(5, 0, random.randint(0, len(SHAPES) - 1))
        
        # Check if the new piece can be placed - if not, game over
        if not self.valid_move(piece, self.grid):
            self.game_over = True
            self.game_over_sound.play()
        return piece

    def valid_move(self, piece, grid, x_offset=0, y_offset=0):
        # Check if a move is valid (within bounds and not overlapping locked pieces)
        for i, row in enumerate(piece.get_shape()):
            for j, cell in enumerate(row):
                if cell == '0':
                    new_x = piece.x + j + x_offset
                    new_y = piece.y + i + y_offset
                    
                    # Check if position is valid horizontally (within grid width)
                    if new_x < 0 or new_x >= 10:
                        return False
                    
                    # Check if piece is overlapping with existing blocks
                    # We only check this if the position is within the visible grid (y >= 0)
                    if new_y >= 0 and new_y < 20 and grid[new_y][new_x] != (0, 0, 0):
                        return False
                    
                    # Check if the piece has reached the bottom
                    if new_y >= 20:
                        return False
                    
        return True

    def draw_text(self, text, font, color, x, y, center=True, shadow=True):
        # Utility function to draw text with shadow for better visibility
        if shadow:
            shadow_surface = font.render(text, True, (0, 0, 0, 160))
            if center:
                self.screen.blit(shadow_surface, (x - shadow_surface.get_width() // 2 + 2, 
                                                 y - shadow_surface.get_height() // 2 + 2))
            else:
                self.screen.blit(shadow_surface, (x + 2, y + 2))
        
        text_surface = font.render(text, True, color)
        if center:
            self.screen.blit(text_surface, (x - text_surface.get_width() // 2, 
                                           y - text_surface.get_height() // 2))
        else:
            self.screen.blit(text_surface, (x, y))

    def draw_grid_lines(self):
        # Draw the grid lines for the play area with fade effect
        line_color = GRAY
        for i in range(21):  # horizontal lines (21 for bottom line)
            line_opacity = min(255, 100 + i * 8)  # Lines get more visible toward the bottom
            current_color = (line_color[0], line_color[1], line_color[2], line_opacity)
            pygame.draw.line(self.screen, current_color, 
                             (TOP_LEFT_X, TOP_LEFT_Y + i * BLOCK_SIZE),
                             (TOP_LEFT_X + PLAY_WIDTH, TOP_LEFT_Y + i * BLOCK_SIZE))
        
        for j in range(11):  # vertical lines (11 for right line)
            pygame.draw.line(self.screen, line_color, 
                             (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y),
                             (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + PLAY_HEIGHT))

    def draw_grid_blocks(self):
        # Draw the blocks in the grid with enhanced 3D effect
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                color = self.grid[i][j]
                if color != (0, 0, 0):  # If not black (empty)
                    x = TOP_LEFT_X + j * BLOCK_SIZE
                    y = TOP_LEFT_Y + i * BLOCK_SIZE
                    
                    # Draw main block with rounded corners
                    pygame.draw.rect(self.screen, color, 
                                    (x, y, BLOCK_SIZE, BLOCK_SIZE), 0, 2)
                    
                    # Draw 3D effect - top and left edges lighter
                    pygame.draw.line(self.screen, self.lighten_color(color), 
                                    (x, y), (x + BLOCK_SIZE - 1, y), 2)
                    pygame.draw.line(self.screen, self.lighten_color(color), 
                                    (x, y), (x, y + BLOCK_SIZE - 1), 2)
                    
                    # Draw 3D effect - bottom and right edges darker
                    pygame.draw.line(self.screen, self.darken_color(color), 
                                    (x, y + BLOCK_SIZE - 1), (x + BLOCK_SIZE - 1, y + BLOCK_SIZE - 1), 2)
                    pygame.draw.line(self.screen, self.darken_color(color), 
                                    (x + BLOCK_SIZE - 1, y), (x + BLOCK_SIZE - 1, y + BLOCK_SIZE - 1), 2)
                    
                    # Draw inner shading for 3D effect
                    inner_color = self.lighten_color(color, 0.2)
                    pygame.draw.rect(self.screen, inner_color, 
                                   (x + 4, y + 4, BLOCK_SIZE - 8, BLOCK_SIZE - 8), 0, 1)

    def darken_color(self, color, factor=0.7):
        # Utility function to darken a color for 3D effect
        return (max(0, int(color[0] * factor)), 
                max(0, int(color[1] * factor)), 
                max(0, int(color[2] * factor)))

    def lighten_color(self, color, factor=0.3):
        # Utility function to lighten a color for 3D effect
        return (min(255, int(color[0] + (255 - color[0]) * factor)), 
                min(255, int(color[1] + (255 - color[1]) * factor)), 
                min(255, int(color[2] + (255 - color[2]) * factor)))

    def draw_piece(self, piece, ghost=False):
        # Draw the current piece with enhanced 3D effect
        shape = piece.get_shape()
        
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell == '0':
                    x = TOP_LEFT_X + (piece.x + j) * BLOCK_SIZE
                    y = TOP_LEFT_Y + (piece.y + i) * BLOCK_SIZE
                    
                    if not ghost:
                        # Draw the piece with enhanced 3D effect
                        pygame.draw.rect(self.screen, piece.color, 
                                        (x, y, BLOCK_SIZE, BLOCK_SIZE), 0, 2)
                        
                        # Draw 3D effect - top and left edges lighter
                        pygame.draw.line(self.screen, self.lighten_color(piece.color), 
                                        (x, y), (x + BLOCK_SIZE - 1, y), 2)
                        pygame.draw.line(self.screen, self.lighten_color(piece.color), 
                                        (x, y), (x, y + BLOCK_SIZE - 1), 2)
                        
                        # Draw 3D effect - bottom and right edges darker
                        pygame.draw.line(self.screen, self.darken_color(piece.color), 
                                        (x, y + BLOCK_SIZE - 1), (x + BLOCK_SIZE - 1, y + BLOCK_SIZE - 1), 2)
                        pygame.draw.line(self.screen, self.darken_color(piece.color), 
                                        (x + BLOCK_SIZE - 1, y), (x + BLOCK_SIZE - 1, y + BLOCK_SIZE - 1), 2)
                        
                        # Draw inner shading for 3D effect
                        inner_color = self.lighten_color(piece.color, 0.2)
                        pygame.draw.rect(self.screen, inner_color, 
                                       (x + 4, y + 4, BLOCK_SIZE - 8, BLOCK_SIZE - 8), 0, 1)
                    else:
                        # Draw ghost piece with semi-transparent effect
                        ghost_color = (piece.color[0], piece.color[1], piece.color[2], 70)
                        s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                        s.fill(ghost_color)
                        self.screen.blit(s, (x, y))
                        pygame.draw.rect(self.screen, (255, 255, 255, 180), 
                                        (x, y, BLOCK_SIZE, BLOCK_SIZE), 1, 1)

    def draw_ghost_piece(self):
        # Create a "ghost" piece that shows where the current piece will land
        ghost_piece = Piece(self.current_piece.x, self.current_piece.y, self.current_piece.shape_index)
        ghost_piece.rotation = self.current_piece.rotation
        
        # Move the ghost piece down until it hits something
        while self.valid_move(ghost_piece, self.grid, 0, 1):
            ghost_piece.y += 1
        
        # Draw the ghost piece
        if ghost_piece.y > self.current_piece.y:
            self.draw_piece(ghost_piece, ghost=True)

    def draw_next_piece(self):
        # Draw the next piece preview with enhanced UI
        panel_x = TOP_LEFT_X + PLAY_WIDTH + 50
        panel_y = TOP_LEFT_Y + 50  # Moved up by 20px to prevent overflow
        
        # Draw panel background
        self.screen.blit(self.panel_next, (panel_x - 20, panel_y - 20))
        
        # Draw header
        self.draw_text("KÖVETKEZŐ", FONT_MEDIUM, WHITE, panel_x + PREVIEW_SIZE, panel_y - 10)
        
        # Draw the next piece with enhanced 3D effect
        shape = self.next_piece.get_shape()
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell == '0':
                    x = panel_x + j * (BLOCK_SIZE // 1.5)
                    y = panel_y + 20 + i * (BLOCK_SIZE // 1.5)
                    block_size = BLOCK_SIZE // 1.5
                    
                    # Draw block with 3D effect
                    pygame.draw.rect(self.screen, self.next_piece.color, 
                                    (x, y, block_size, block_size), 0, 1)
                    
                    # 3D effect edges
                    pygame.draw.line(self.screen, self.lighten_color(self.next_piece.color), 
                                    (x, y), (x + block_size - 1, y), 1)
                    pygame.draw.line(self.screen, self.lighten_color(self.next_piece.color), 
                                    (x, y), (x, y + block_size - 1), 1)
                    pygame.draw.line(self.screen, self.darken_color(self.next_piece.color), 
                                    (x, y + block_size - 1), (x + block_size - 1, y + block_size - 1), 1)
                    pygame.draw.line(self.screen, self.darken_color(self.next_piece.color), 
                                    (x + block_size - 1, y), (x + block_size - 1, y + block_size - 1), 1)

    def draw_score(self):
        # Draw score, level, and lines cleared with enhanced UI
        panel_x = TOP_LEFT_X + PLAY_WIDTH + 50
        score_y = TOP_LEFT_Y + 200
        level_y = TOP_LEFT_Y + 290
        lines_y = TOP_LEFT_Y + 380
        
        # Animate score when it changes
        score_color = WHITE
        if time.time() * 1000 - self.last_score_increase < 500:
            pulse = abs(math.sin(time.time() * 10)) 
            score_color = (255, 255 * (1-pulse), 255 * (1-pulse))
        
        # Score panel
        self.screen.blit(self.panel_score, (panel_x - 20, score_y - 20))
        self.draw_text("PONTSZÁM", FONT_MEDIUM, WHITE, panel_x + 80, score_y)
        self.draw_text(str(self.score), FONT_MEDIUM, score_color, panel_x + 80, score_y + 30)
        
        # Level panel
        self.screen.blit(self.panel_score, (panel_x - 20, level_y - 20))
        self.draw_text("SZINT", FONT_MEDIUM, WHITE, panel_x + 80, level_y)
        self.draw_text(str(self.level), FONT_MEDIUM, MODERN_GREEN, panel_x + 80, level_y + 30)
        
        # Lines panel
        self.screen.blit(self.panel_score, (panel_x - 20, lines_y - 20))
        self.draw_text("SOROK", FONT_MEDIUM, WHITE, panel_x + 80, lines_y)
        self.draw_text(str(self.lines_cleared), FONT_MEDIUM, MODERN_BLUE, panel_x + 80, lines_y + 30)
        
        if self.combo > 1:
            combo_y = TOP_LEFT_Y + 470
            combo_color = MODERN_YELLOW
            pulse = abs(math.sin(time.time() * 5))
            combo_scale = 1 + pulse * 0.2
            combo_font = pygame.font.Font(None, int(36 * combo_scale))
            self.draw_text(f"COMBO x{self.combo}", combo_font, combo_color, panel_x + 80, combo_y)

    def draw_controls(self):
        # Draw controls with enhanced UI
        panel_x = TOP_LEFT_X - 220 # Adjusted X position further left
        panel_y = TOP_LEFT_Y + 100
        
        # Draw panel background
        self.screen.blit(self.panel_controls, (panel_x - 20, panel_y - 20))
        
        # Draw control instructions
        controls = [
            "IRÁNYÍTÁS:",
            "← → : Mozgatás",
            "↓ : Gyors esés",
            "↑ : Forgatás",
            "SPACE : Azonnali esés",
            "P : Szünet",
            "R : Újraindítás"
        ]
        
        for i, text in enumerate(controls):
            color = WHITE if i == 0 else LIGHT_GRAY
            self.draw_text(text, FONT_SMALL, color, panel_x + 80, panel_y + 20 + i * 26, center=True, shadow=True) # Centered text within the panel

    def draw_game_over(self):
        # Draw game over screen with enhanced UI
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black overlay
        self.screen.blit(overlay, (0, 0))
        
        # Create animated pulse effect
        pulse = abs(math.sin(time.time() * 2)) 
        pulse_scale = 1 + pulse * 0.1
        game_over_font = pygame.font.Font(None, int(60 * pulse_scale))
        
        # Draw game over text
        self.draw_text("JÁTÉK VÉGE", game_over_font, MODERN_RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        self.draw_text(f"Végső pontszám: {self.score}", FONT_MEDIUM, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
        self.draw_text("Nyomd meg az R billentyűt az újraindításhoz", FONT_MEDIUM, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70)

    def draw_pause(self):
        # Draw pause screen with enhanced UI
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black overlay
        self.screen.blit(overlay, (0, 0))
        
        # Create animated pulse effect
        pulse = abs(math.sin(time.time() * 2)) 
        pulse_scale = 1 + pulse * 0.1
        pause_font = pygame.font.Font(None, int(60 * pulse_scale))
        
        # Draw pause text
        self.draw_text("SZÜNETELTETVE", pause_font, MODERN_YELLOW, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.draw_text("Nyomd meg a P billentyűt a folytatáshoz", FONT_MEDIUM, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70)

    def draw_background(self):
        # Draw animated gradient background
        for y in range(0, SCREEN_HEIGHT, 2):
            # Calculate gradient color with time-based wave
            gradient_factor = y / SCREEN_HEIGHT
            wave = math.sin(time.time() * 0.5 + y * 0.01) * 0.1
            gradient_factor = max(0, min(1, gradient_factor + wave))
            
            r = int(BG_COLOR_1[0] * (1 - gradient_factor) + BG_COLOR_2[0] * gradient_factor)
            g = int(BG_COLOR_1[1] * (1 - gradient_factor) + BG_COLOR_2[1] * gradient_factor)
            b = int(BG_COLOR_1[2] * (1 - gradient_factor) + BG_COLOR_2[2] * gradient_factor)
            color = (r, g, b)
            
            # Draw horizontal line of the gradient
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
        
        # Add subtle grid pattern overlay
        grid_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        grid_overlay.fill((0, 0, 0, 0))
        
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(grid_overlay, (255, 255, 255, 10), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.line(grid_overlay, (255, 255, 255, 10), (0, y), (SCREEN_WIDTH, y))
            
        self.screen.blit(grid_overlay, (0, 0))

    def draw_window(self):
        # Draw background
        self.draw_background()
        
        # Update animation time
        self.animation_time = time.time()
        
        # Draw title with glow effect
        title_y = 40
        glow_size = abs(math.sin(self.animation_time)) * 10 + 5
        # Draw glow
        for i in range(3):
            size = int(glow_size * (3-i)/3)
            alpha = 100 - i * 30
            glow_text = pygame.font.Font(None, 60 + size).render("MODERN TETRIS", True, (255, 255, 255, alpha))
            self.screen.blit(glow_text, 
                            (SCREEN_WIDTH // 2 - glow_text.get_width() // 2, 
                             title_y - glow_text.get_height() // 2))
        
        # Draw actual title text
        self.draw_text("MODERN TETRIS", FONT_LARGE, WHITE, SCREEN_WIDTH // 2, title_y)
        
        # Draw game area background
        self.screen.blit(self.panel_main, (TOP_LEFT_X - 20, TOP_LEFT_Y - 20))
        
        # Draw grid, pieces, and UI elements if game not over
        self.draw_grid_blocks()
        self.draw_grid_lines()
        
        if not self.game_over:
            self.draw_ghost_piece()
            self.draw_piece(self.current_piece)
        
        self.draw_next_piece()
        self.draw_score()
        self.draw_controls()
        
        # Draw game over or pause screen if needed
        if self.game_over:
            self.draw_game_over()
        elif self.paused:
            self.draw_pause()
        
        # Update display
        pygame.display.update()

    def hard_drop(self):
        # Drop the piece all the way down
        while self.valid_move(self.current_piece, self.grid, 0, 1):
            self.current_piece.y += 1
        
        # Add score for hard drop (2 points per cell dropped)
        drop_points = 2 * (self.current_piece.y - self.get_new_piece().y)
        self.score += drop_points
        
        # Lock the piece and get a new one
        self.lock_piece()
        self.fall_sound.play()

    def lock_piece(self):
        # Lock the current piece in place and get a new one
        shape = self.current_piece.get_shape()
        
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell == '0':
                    # Check if any part of the piece is above the play area (game over)
                    if self.current_piece.y + i < 0:
                        self.game_over = True
                        self.game_over_sound.play()
                        return
                    
                    # Add position to locked positions
                    self.locked_positions[(self.current_piece.x + j, self.current_piece.y + i)] = self.current_piece.color
        
        # Update grid with locked positions
        self.update_grid()
        
        # Check for cleared lines
        cleared_lines = self.clear_lines()
        
        # Update combo counter
        if cleared_lines > 0:
            self.combo += 1
        else:
            self.combo = 0
            
        # Update score based on cleared lines
        if cleared_lines == 1:
            self.score += 100 * self.level
            self.last_score_increase = time.time() * 1000
            self.clear_sound.play()
        elif cleared_lines == 2:
            self.score += 300 * self.level
            self.last_score_increase = time.time() * 1000
            self.clear_sound.play()
        elif cleared_lines == 3:
            self.score += 500 * self.level
            self.last_score_increase = time.time() * 1000
            self.clear_sound.play()
        elif cleared_lines == 4:  # Tetris!
            self.score += 800 * self.level
            self.last_score_increase = time.time() * 1000
            self.clear_sound.play()
        
        # Add combo bonus
        if self.combo > 1 and cleared_lines > 0:
            self.score += 50 * self.combo * self.level
            self.last_score_increase = time.time() * 1000
        
        # Update lines cleared and check for level up
        self.lines_cleared += cleared_lines
        self.level = (self.lines_cleared // 10) + 1
        
        # Update drop speed based on level (faster as level increases)
        self.drop_speed = max(100, 500 - (self.level - 1) * 20)
        
        # Get the next piece
        self.current_piece = self.next_piece
        self.next_piece = self.get_new_piece()

    def clear_lines(self):
        # Check for completed lines and clear them
        lines_to_clear = []
        
        for i, row in enumerate(self.grid):
            if all(color != (0, 0, 0) for color in row):
                lines_to_clear.append(i)
        
        if not lines_to_clear:
            return 0
            
        # Remove complete lines and add empty lines at the top
        for line in sorted(lines_to_clear, reverse=True):
            # Remove the line
            for key in sorted(list(self.locked_positions.keys()), key=lambda x: x[1], reverse=True):
                x, y = key
                
                if y < line:
                    # Move blocks above the cleared line down
                    new_key = (x, y + 1)
                    self.locked_positions[new_key] = self.locked_positions[key]
                    del self.locked_positions[key]
                elif y == line:
                    # Remove blocks in the cleared line
                    del self.locked_positions[key]
        
        # Update grid
        self.update_grid()
        
        return len(lines_to_clear)

    def run(self):
        # Main game loop
        running = True
        
        while running:
            # Check for time-based actions
            current_time = time.time() * 1000
            
            # Normal gravity drop if not paused or game over
            if not self.paused and not self.game_over:
                if current_time - self.last_drop_time > self.drop_speed:
                    self.last_drop_time = current_time
                    
                    if self.valid_move(self.current_piece, self.grid, 0, 1):
                        self.current_piece.y += 1
                    else:
                        self.lock_piece()
            
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Key press events
                if event.type == pygame.KEYDOWN:
                    # Game control keys
                    if event.key == pygame.K_p:  # Pause
                        self.paused = not self.paused
                    
                    if event.key == pygame.K_r:  # Restart
                        self.reset_game()
                    
                    # Only process movement if not paused and not game over
                    if not self.paused and not self.game_over:
                        if event.key == pygame.K_LEFT:
                            if self.valid_move(self.current_piece, self.grid, -1, 0):
                                self.current_piece.x -= 1
                                self.move_sound.play()
                            self.last_move_time[pygame.K_LEFT] = current_time
                            
                        elif event.key == pygame.K_RIGHT:
                            if self.valid_move(self.current_piece, self.grid, 1, 0):
                                self.current_piece.x += 1
                                self.move_sound.play()
                            self.last_move_time[pygame.K_RIGHT] = current_time
                            
                        elif event.key == pygame.K_DOWN:
                            self.down_pressed = True
                            self.last_move_time[pygame.K_DOWN] = current_time
                            
                        elif event.key == pygame.K_UP:  # Rotate
                            # Save current rotation
                            old_rotation = self.current_piece.rotation
                            
                            # Try to rotate
                            self.current_piece.rotation += 1
                            
                            # If rotation is not valid, try wall kicks
                            if not self.valid_move(self.current_piece, self.grid):
                                # Try to move right if blocked on left
                                if self.valid_move(self.current_piece, self.grid, 1, 0):
                                    self.current_piece.x += 1
                                # Try to move left if blocked on right
                                elif self.valid_move(self.current_piece, self.grid, -1, 0):
                                    self.current_piece.x -= 1
                                # Try to move up if blocked below
                                elif self.valid_move(self.current_piece, self.grid, 0, -1):
                                    self.current_piece.y -= 1
                                else:
                                    # If all fails, revert rotation
                                    self.current_piece.rotation = old_rotation
                            
                            if self.current_piece.rotation != old_rotation:
                                self.rotate_sound.play()
                            
                        elif event.key == pygame.K_SPACE:  # Hard drop
                            self.hard_drop()
                
                # Key release events
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.down_pressed = False
            
            # Handle held keys (continuous movement)
            keys = pygame.key.get_pressed()
            
            if not self.paused and not self.game_over:
                # Handle left/right movement with repeat delay
                if keys[pygame.K_LEFT] and current_time - self.last_move_time[pygame.K_LEFT] > self.move_repeat_delay:
                    if self.valid_move(self.current_piece, self.grid, -1, 0):
                        self.current_piece.x -= 1
                        self.last_move_time[pygame.K_LEFT] = current_time
                
                if keys[pygame.K_RIGHT] and current_time - self.last_move_time[pygame.K_RIGHT] > self.move_repeat_delay:
                    if self.valid_move(self.current_piece, self.grid, 1, 0):
                        self.current_piece.x += 1
                        self.last_move_time[pygame.K_RIGHT] = current_time
                
                # Handle soft drop (faster fall when down is held)
                if self.down_pressed and current_time - self.last_move_time[pygame.K_DOWN] > self.move_repeat_delay / 2:
                    if self.valid_move(self.current_piece, self.grid, 0, 1):
                        self.current_piece.y += 1
                        self.score += 1  # Small score bonus for soft drop
                        self.last_move_time[pygame.K_DOWN] = current_time
            
            # Draw everything
            self.draw_window()
            
            # Cap the frame rate
            self.clock.tick(60)
        
        # Quit pygame when done
        pygame.quit()

# Start the game when the script is run
if __name__ == "__main__":
    game = Tetris()
    game.run()