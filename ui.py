import pygame
import math
import time
from config import *

class UI:
    """
    A Tetris játék felhasználói felületét kezelő osztály.
    Gondoskodik a játéktér, pontszám, elemek stb. megjelenítéséről.
    """
    def __init__(self, screen):
        """
        Inicializálja a felhasználói felületet.
        
        Args:
            screen: A pygame képernyő objektum
        """
        self.screen = screen
        self.animation_time = 0
        self.score_flash = 0
        self.create_ui_panels()
        
    def create_ui_panels(self):
        """Létrehozza az UI panel háttereket."""
        self.panel_main = self.create_panel(PLAY_WIDTH + 40, PLAY_HEIGHT + 40, 10)
        self.panel_next = self.create_panel(PREVIEW_SIZE * 2 + 40, PREVIEW_SIZE * 2 + 40, 5)
        self.panel_score = self.create_panel(200, 80, 5)
        self.panel_controls = self.create_panel(200, 220, 5)
        
    def create_panel(self, width, height, border_radius):
        """
        Létrehoz egy panelt lekerekített sarkokkal és színátmenettel.
        
        Args:
            width: A panel szélessége
            height: A panel magassága
            border_radius: A sarkok lekerekítésének sugara
            
        Returns:
            A kész panel felülete (Surface)
        """
        panel = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Gradiens háttér
        for y in range(height):
            gradient_factor = y / height
            r = int(DARK_GRAY[0] * (1 - gradient_factor) + BG_COLOR_1[0] * gradient_factor)
            g = int(DARK_GRAY[1] * (1 - gradient_factor) + BG_COLOR_1[1] * gradient_factor)
            b = int(DARK_GRAY[2] * (1 - gradient_factor) + BG_COLOR_1[2] * gradient_factor)
            color = (r, g, b, 180)  # Félig átlátszó
            
            pygame.draw.line(panel, color, (0, y), (width, y))
        
        # Lekerekített téglalap keret
        pygame.draw.rect(panel, WHITE, (0, 0, width, height), 2, border_radius)
        
        return panel
        
    def draw_text(self, text, font, color, x, y, center=True, shadow=True):
        """
        Szöveg kirajzolása, opcionálisan árnyékkal.
        
        Args:
            text: A megjelenítendő szöveg
            font: A használt betűtípus
            color: A szöveg színe
            x, y: A pozíció
            center: Középre igazítás (True) vagy balra igazítás (False)
            shadow: Árnyék hozzáadása
        """
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
    
    def darken_color(self, color, factor=0.7):
        """
        Egy szín sötétítése a 3D hatáshoz.
        
        Args:
            color: Az eredeti szín
            factor: A sötétítés mértéke (0-1 között)
            
        Returns:
            A sötétített szín
        """
        return (max(0, int(color[0] * factor)), 
                max(0, int(color[1] * factor)), 
                max(0, int(color[2] * factor)))

    def lighten_color(self, color, factor=0.3):
        """
        Egy szín világosítása a 3D hatáshoz.
        
        Args:
            color: Az eredeti szín
            factor: A világosítás mértéke (0-1 között)
            
        Returns:
            A világosított szín
        """
        return (min(255, int(color[0] + (255 - color[0]) * factor)), 
                min(255, int(color[1] + (255 - color[1]) * factor)), 
                min(255, int(color[2] + (255 - color[2]) * factor)))
                
    def draw_background(self):
        """Animált háttér rajzolása."""
        for y in range(0, SCREEN_HEIGHT, 2):
            # Színátmenet számítása időalapú hullámzással
            gradient_factor = y / SCREEN_HEIGHT
            wave = math.sin(time.time() * 0.5 + y * 0.01) * 0.1
            gradient_factor = max(0, min(1, gradient_factor + wave))
            
            r = int(BG_COLOR_1[0] * (1 - gradient_factor) + BG_COLOR_2[0] * gradient_factor)
            g = int(BG_COLOR_1[1] * (1 - gradient_factor) + BG_COLOR_2[1] * gradient_factor)
            b = int(BG_COLOR_1[2] * (1 - gradient_factor) + BG_COLOR_2[2] * gradient_factor)
            color = (r, g, b)
            
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
        
        # Finom rácsminta az átlátszó háttérre
        grid_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        grid_overlay.fill((0, 0, 0, 0))
        
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(grid_overlay, (255, 255, 255, 10), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.line(grid_overlay, (255, 255, 255, 10), (0, y), (SCREEN_WIDTH, y))
            
        self.screen.blit(grid_overlay, (0, 0))
        
    def draw_title(self):
        """Animált cím rajzolása."""
        title_y = 40
        self.animation_time = time.time()
        glow_size = abs(math.sin(self.animation_time)) * 10 + 5
        
        # Ragyogás rajzolása
        for i in range(3):
            size = int(glow_size * (3-i)/3)
            alpha = 100 - i * 30
            glow_text = pygame.font.Font(None, 60 + size).render("MODERN TETRIS", True, (255, 255, 255, alpha))
            self.screen.blit(glow_text, 
                           (SCREEN_WIDTH // 2 - glow_text.get_width() // 2, 
                            title_y - glow_text.get_height() // 2))
        
        # Tényleges címszöveg rajzolása
        self.draw_text("MODERN TETRIS", FONT_LARGE, WHITE, SCREEN_WIDTH // 2, title_y)
        
    def draw_grid_lines(self):
        """Játéktér rácsvonalainak rajzolása halvány effekttel."""
        line_color = GRAY
        for i in range(21):  # vízszintes vonalak (21 a legalsó vonalnak)
            line_opacity = min(255, 100 + i * 8)  # A vonalak láthatóbbak lesznek lefelé haladva
            current_color = (line_color[0], line_color[1], line_color[2], line_opacity)
            pygame.draw.line(self.screen, current_color, 
                            (TOP_LEFT_X, TOP_LEFT_Y + i * BLOCK_SIZE),
                            (TOP_LEFT_X + PLAY_WIDTH, TOP_LEFT_Y + i * BLOCK_SIZE))
        
        for j in range(11):  # függőleges vonalak (11 a jobb oldali vonalnak)
            pygame.draw.line(self.screen, line_color, 
                            (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y),
                            (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + PLAY_HEIGHT))
    
    def draw_grid_blocks(self, grid):
        """
        A rögzített blokkok rajzolása a játéktérre.
        
        Args:
            grid: A játéktér rácsa, amely tartalmazza a blokkok színeit
        """
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                color = grid[i][j]
                if color != (0, 0, 0):  # Ha nem fekete (üres)
                    x = TOP_LEFT_X + j * BLOCK_SIZE
                    y = TOP_LEFT_Y + i * BLOCK_SIZE
                    
                    # Fő blokk rajzolása lekerekített sarkokkal
                    pygame.draw.rect(self.screen, color, 
                                   (x, y, BLOCK_SIZE, BLOCK_SIZE), 0, 2)
                    
                    # 3D hatás - felső és bal élek világosabbak
                    pygame.draw.line(self.screen, self.lighten_color(color), 
                                   (x, y), (x + BLOCK_SIZE - 1, y), 2)
                    pygame.draw.line(self.screen, self.lighten_color(color), 
                                   (x, y), (x, y + BLOCK_SIZE - 1), 2)
                    
                    # 3D hatás - alsó és jobb élek sötétebbek
                    pygame.draw.line(self.screen, self.darken_color(color), 
                                   (x, y + BLOCK_SIZE - 1), (x + BLOCK_SIZE - 1, y + BLOCK_SIZE - 1), 2)
                    pygame.draw.line(self.screen, self.darken_color(color), 
                                   (x + BLOCK_SIZE - 1, y), (x + BLOCK_SIZE - 1, y + BLOCK_SIZE - 1), 2)
                    
                    # Belső árnyékolás a 3D hatáshoz
                    inner_color = self.lighten_color(color, 0.2)
                    pygame.draw.rect(self.screen, inner_color, 
                                  (x + 4, y + 4, BLOCK_SIZE - 8, BLOCK_SIZE - 8), 0, 1)
                    
    def draw_piece(self, piece, ghost=False):
        """
        Tetris elem rajzolása.
        
        Args:
            piece: A rajzolandó Piece objektum
            ghost: Ha True, akkor átlátszó "szellem" előnézetet rajzol
        """
        shape = piece.get_shape()
        
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell == '0':
                    x = TOP_LEFT_X + (piece.x + j) * BLOCK_SIZE
                    y = TOP_LEFT_Y + (piece.y + i) * BLOCK_SIZE
                    
                    if not ghost:
                        # Elem rajzolása továbbfejlesztett 3D hatással
                        pygame.draw.rect(self.screen, piece.color, 
                                       (x, y, BLOCK_SIZE, BLOCK_SIZE), 0, 2)
                        
                        # 3D hatás - felső és bal élek világosabbak
                        pygame.draw.line(self.screen, self.lighten_color(piece.color), 
                                       (x, y), (x + BLOCK_SIZE - 1, y), 2)
                        pygame.draw.line(self.screen, self.lighten_color(piece.color), 
                                       (x, y), (x, y + BLOCK_SIZE - 1), 2)
                        
                        # 3D hatás - alsó és jobb élek sötétebbek
                        pygame.draw.line(self.screen, self.darken_color(piece.color), 
                                       (x, y + BLOCK_SIZE - 1), (x + BLOCK_SIZE - 1, y + BLOCK_SIZE - 1), 2)
                        pygame.draw.line(self.screen, self.darken_color(piece.color), 
                                       (x + BLOCK_SIZE - 1, y), (x + BLOCK_SIZE - 1, y + BLOCK_SIZE - 1), 2)
                        
                        # Belső árnyékolás a 3D hatáshoz
                        inner_color = self.lighten_color(piece.color, 0.2)
                        pygame.draw.rect(self.screen, inner_color, 
                                      (x + 4, y + 4, BLOCK_SIZE - 8, BLOCK_SIZE - 8), 0, 1)
                    else:
                        # "Szellem" elem rajzolása félig átlátszó hatással
                        ghost_color = (piece.color[0], piece.color[1], piece.color[2], 70)
                        s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                        s.fill(ghost_color)
                        self.screen.blit(s, (x, y))
                        pygame.draw.rect(self.screen, (255, 255, 255, 180), 
                                       (x, y, BLOCK_SIZE, BLOCK_SIZE), 1, 1)
                      
    def draw_next_piece(self, next_piece):
        """
        A következő elem előnézetének rajzolása.
        
        Args:
            next_piece: A következő Piece objektum
        """
        panel_x = TOP_LEFT_X + PLAY_WIDTH + 50
        panel_y = TOP_LEFT_Y + 50  # Feljebb került 20px-el az átlapolás elkerülése érdekében
        
        # Panel háttér rajzolása
        self.screen.blit(self.panel_next, (panel_x - 20, panel_y - 20))
        
        # Fejléc rajzolása
        self.draw_text("KÖVETKEZŐ", FONT_MEDIUM, WHITE, panel_x + PREVIEW_SIZE, panel_y - 10)
        
        # Következő elem rajzolása továbbfejlesztett 3D hatással
        shape = next_piece.get_shape()
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell == '0':
                    x = panel_x + j * (BLOCK_SIZE // 1.5)
                    y = panel_y + 20 + i * (BLOCK_SIZE // 1.5)
                    block_size = BLOCK_SIZE // 1.5
                    
                    # Blokk rajzolása 3D hatással
                    pygame.draw.rect(self.screen, next_piece.color, 
                                   (x, y, block_size, block_size), 0, 1)
                    
                    # 3D hatás élek
                    pygame.draw.line(self.screen, self.lighten_color(next_piece.color), 
                                   (x, y), (x + block_size - 1, y), 1)
                    pygame.draw.line(self.screen, self.lighten_color(next_piece.color), 
                                   (x, y), (x, y + block_size - 1), 1)
                    pygame.draw.line(self.screen, self.darken_color(next_piece.color), 
                                   (x, y + block_size - 1), (x + block_size - 1, y + block_size - 1), 1)
                    pygame.draw.line(self.screen, self.darken_color(next_piece.color), 
                                   (x + block_size - 1, y), (x + block_size - 1, y + block_size - 1), 1)

    def draw_score(self, score, level, lines_cleared, combo, last_score_increase):
        """
        A pontszám, szint és kitörölt sorok számának megjelenítése.
        
        Args:
            score: Játékos pontszáma
            level: Játék szintje
            lines_cleared: Kitörölt sorok száma
            combo: Combo szám (ha van)
            last_score_increase: Utolsó pontszám növekedés időpontja
        """
        panel_x = TOP_LEFT_X + PLAY_WIDTH + 50
        score_y = TOP_LEFT_Y + 200
        level_y = TOP_LEFT_Y + 290
        lines_y = TOP_LEFT_Y + 380
        
        # Pontszám animáció amikor változik
        score_color = WHITE
        if time.time() * 1000 - last_score_increase < 500:
            pulse = abs(math.sin(time.time() * 10)) 
            score_color = (255, 255 * (1-pulse), 255 * (1-pulse))
        
        # Pontszám panel
        self.screen.blit(self.panel_score, (panel_x - 20, score_y - 20))
        self.draw_text("PONTSZÁM", FONT_MEDIUM, WHITE, panel_x + 80, score_y)
        self.draw_text(str(score), FONT_MEDIUM, score_color, panel_x + 80, score_y + 30)
        
        # Szint panel
        self.screen.blit(self.panel_score, (panel_x - 20, level_y - 20))
        self.draw_text("SZINT", FONT_MEDIUM, WHITE, panel_x + 80, level_y)
        self.draw_text(str(level), FONT_MEDIUM, MODERN_GREEN, panel_x + 80, level_y + 30)
        
        # Sorok panel
        self.screen.blit(self.panel_score, (panel_x - 20, lines_y - 20))
        self.draw_text("SOROK", FONT_MEDIUM, WHITE, panel_x + 80, lines_y)
        self.draw_text(str(lines_cleared), FONT_MEDIUM, MODERN_BLUE, panel_x + 80, lines_y + 30)
        
        # Combo megjelenítése, ha van
        if combo > 1:
            combo_y = TOP_LEFT_Y + 470
            combo_color = MODERN_YELLOW
            pulse = abs(math.sin(time.time() * 5))
            combo_scale = 1 + pulse * 0.2
            combo_font = pygame.font.Font(None, int(36 * combo_scale))
            self.draw_text(f"COMBO x{combo}", combo_font, combo_color, panel_x + 80, combo_y)

    def draw_controls(self):
        """Irányítási útmutató megjelenítése."""
        panel_x = TOP_LEFT_X - 220  # Balra igazítva, hogy ne lógjon a játéktérre
        panel_y = TOP_LEFT_Y + 100
        
        # Panel háttér
        self.screen.blit(self.panel_controls, (panel_x - 20, panel_y - 20))
        
        # Irányítási utasítások
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
            self.draw_text(text, FONT_SMALL, color, panel_x + 80, panel_y + 20 + i * 26, center=True, shadow=True)

    def draw_game_over(self, score):
        """
        Játék vége képernyő megjelenítése.
        
        Args:
            score: Végső pontszám
        """
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Félig átlátszó fekete fedőréteg
        self.screen.blit(overlay, (0, 0))
        
        # Animált pulzáló effektus létrehozása
        pulse = abs(math.sin(time.time() * 2)) 
        pulse_scale = 1 + pulse * 0.1
        game_over_font = pygame.font.Font(None, int(60 * pulse_scale))
        
        # Játék vége szöveg
        self.draw_text("JÁTÉK VÉGE", game_over_font, MODERN_RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        self.draw_text(f"Végső pontszám: {score}", FONT_MEDIUM, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
        self.draw_text("Nyomd meg az R billentyűt az újraindításhoz", FONT_MEDIUM, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70)

    def draw_pause(self):
        """Szüneteltetés képernyő megjelenítése."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Félig átlátszó fekete fedőréteg
        self.screen.blit(overlay, (0, 0))
        
        # Animált pulzáló effektus létrehozása
        pulse = abs(math.sin(time.time() * 2)) 
        pulse_scale = 1 + pulse * 0.1
        pause_font = pygame.font.Font(None, int(60 * pulse_scale))
        
        # Szüneteltetés szöveg
        self.draw_text("SZÜNETELTETVE", pause_font, MODERN_YELLOW, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.draw_text("Nyomd meg a P billentyűt a folytatáshoz", FONT_MEDIUM, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70)