import pygame
import random
import time
from pygame import mixer
from config import *
from piece import Piece
from ui import UI

class TetrisGame:
    """
    A Tetris játék fő logikáját kezelő osztály.
    Ez az osztály felelős a játék állapotának kezeléséért, elemek mozgatásáért,
    játéktér frissítéséért és játékmenet irányításáért.
    """
    def __init__(self):
        """Inicializálja a játékot."""
        # Pygame inicializálása
        pygame.init()
        mixer.init()
        
        # Képernyő létrehozása
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Modern Tetris - Készítette: GitHub Copilot')
        self.clock = pygame.time.Clock()
        
        # UI inicializálása
        self.ui = UI(self.screen)
        
        # Játék alapállapotba állítása
        self.reset_game()
        
        # Hangok betöltése
        self._load_sounds()
    
    def _load_sounds(self):
        """Hangok betöltése és beállítása."""
        try:
            self.rotate_sound = mixer.Sound(SOUND_ROTATE)
            self.clear_sound = mixer.Sound(SOUND_CLEAR)
            self.fall_sound = mixer.Sound(SOUND_FALL)
            self.game_over_sound = mixer.Sound(SOUND_GAME_OVER)
            self.move_sound = mixer.Sound(SOUND_MOVE)
            
            # Hangerő beállítása
            self.rotate_sound.set_volume(VOLUME_ROTATE)
            self.clear_sound.set_volume(VOLUME_CLEAR)
            self.fall_sound.set_volume(VOLUME_FALL)
            self.game_over_sound.set_volume(VOLUME_GAME_OVER)
            self.move_sound.set_volume(VOLUME_MOVE)
        except:
            # Ha nem sikerül a betöltés, akkor dummy függvények létrehozása
            self.rotate_sound = self.move_sound = self.clear_sound = self.fall_sound = self.game_over_sound = type('obj', (object,), {
                'play': lambda: None
            })
            print("Nem sikerült a hangfájlokat betölteni. Folytatás hang nélkül.")
    
    def reset_game(self):
        """Játék visszaállítása alapállapotba."""
        self.locked_positions = {}
        self.grid = self.create_grid()
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()
        self.game_over = False
        self.paused = False
        
        # Játék statisztikák
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.last_score_increase = 0
        self.combo = 0
        
        # Játék sebesség (milliszekundum / leejtés)
        self.drop_speed = INITIAL_SPEED
        self.last_drop_time = time.time() * 1000
        
        # Irányítás
        self.down_pressed = False
        self.last_move_time = {
            pygame.K_LEFT: 0,
            pygame.K_RIGHT: 0,
            pygame.K_DOWN: 0
        }
        
    def create_grid(self):
        """
        Üres játéktér létrehozása.
        
        Returns:
            list: 20x10-es mátrix, amely a játékteret reprezentálja
        """
        return [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
        
    def update_grid(self):
        """Játéktér frissítése a zárolt elemek alapján."""
        # Először üres rácsot hozunk létre
        self.grid = self.create_grid()
        
        # Hozzáadjuk a zárolt elemeket
        for (j, i), color in self.locked_positions.items():
            if i < 20:  # Ellenőrizzük, hogy a rácsmagasságon belül van-e
                self.grid[i][j] = color
                
    def get_new_piece(self):
        """
        Új véletlen elemet hoz létre.
        
        Returns:
            Piece: Az új elem
        """
        piece = Piece(5, INITIAL_Y_OFFSET, random.randint(0, len(SHAPES) - 1))
        
        # Ellenőrizzük, hogy az új elem elhelyezhető-e - ha nem, játék vége
        if not self.valid_move(piece, self.grid):
            self.game_over = True
            self.game_over_sound.play()
        return piece
        
    def valid_move(self, piece, grid, x_offset=0, y_offset=0):
        """
        Ellenőrzi, hogy egy lépés érvényes-e (határon belül és nem ütközik más elemekkel).
        
        Args:
            piece: Az ellenőrizendő elem
            grid: A játéktér rácsa
            x_offset: X irányú elmozdulás
            y_offset: Y irányú elmozdulás
            
        Returns:
            bool: True ha a lépés érvényes, False ha nem
        """
        for i, row in enumerate(piece.get_shape()):
            for j, cell in enumerate(row):
                if cell == '0':
                    new_x = piece.x + j + x_offset
                    new_y = piece.y + i + y_offset
                    
                    # Ellenőrizzük, hogy vízszintesen érvényes-e a pozíció
                    if new_x < 0 or new_x >= 10:
                        return False
                    
                    # Ellenőrizzük, hogy az elem nem ütközik-e meglévő elemekkel
                    # Csak akkor ellenőrizzük, ha a látható rácson belül van (y >= 0)
                    if new_y >= 0 and new_y < 20 and grid[new_y][new_x] != (0, 0, 0):
                        return False
                    
                    # Ellenőrizzük, hogy az elem elérte-e a játéktér alját
                    if new_y >= 20:
                        return False
                    
        return True
        
    def lock_piece(self):
        """Az aktuális elem rögzítése és új elem létrehozása."""
        shape = self.current_piece.get_shape()
        
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell == '0':
                    # Ellenőrizzük, hogy az elem bármely része a játéktér felett van-e (játék vége)
                    if self.current_piece.y + i < 0:
                        self.game_over = True
                        self.game_over_sound.play()
                        return
                    
                    # Pozíció hozzáadása a zárolt pozíciókhoz
                    self.locked_positions[(self.current_piece.x + j, self.current_piece.y + i)] = self.current_piece.color
        
        # Rács frissítése a zárolt pozíciókkal
        self.update_grid()
        
        # Kitörölt sorok ellenőrzése
        cleared_lines = self.clear_lines()
        
        # Combo számláló frissítése
        if cleared_lines > 0:
            self.combo += 1
        else:
            self.combo = 0
            
        # Pontszám frissítése a kitörölt sorok alapján
        if cleared_lines == 1:
            self.score += SINGLE_LINE_POINTS * self.level
            self.last_score_increase = time.time() * 1000
            self.clear_sound.play()
        elif cleared_lines == 2:
            self.score += DOUBLE_LINE_POINTS * self.level
            self.last_score_increase = time.time() * 1000
            self.clear_sound.play()
        elif cleared_lines == 3:
            self.score += TRIPLE_LINE_POINTS * self.level
            self.last_score_increase = time.time() * 1000
            self.clear_sound.play()
        elif cleared_lines == 4:  # Tetris!
            self.score += TETRIS_POINTS * self.level
            self.last_score_increase = time.time() * 1000
            self.clear_sound.play()
        
        # Combo bónusz hozzáadása
        if self.combo > 1 and cleared_lines > 0:
            self.score += COMBO_POINTS * self.combo * self.level
            self.last_score_increase = time.time() * 1000
        
        # Kitörölt sorok és szint frissítése
        self.lines_cleared += cleared_lines
        self.level = (self.lines_cleared // 10) + 1
        
        # Esési sebesség frissítése a szint alapján (gyorsabb magasabb szinten)
        self.drop_speed = max(MIN_SPEED, INITIAL_SPEED - (self.level - 1) * SPEED_FACTOR)
        
        # Következő elem létrehozása
        self.current_piece = self.next_piece
        self.next_piece = self.get_new_piece()
        
    def clear_lines(self):
        """
        Befejezett sorok ellenőrzése és törlése.
        
        Returns:
            int: A kitörölt sorok száma
        """
        lines_to_clear = []
        
        for i, row in enumerate(self.grid):
            if all(color != (0, 0, 0) for color in row):
                lines_to_clear.append(i)
        
        if not lines_to_clear:
            return 0
            
        # Teljes sorok eltávolítása és üres sorok hozzáadása felülre
        for line in sorted(lines_to_clear, reverse=True):
            # Sor eltávolítása
            for key in sorted(list(self.locked_positions.keys()), key=lambda x: x[1], reverse=True):
                x, y = key
                
                if y < line:
                    # A törölt sor feletti blokkok mozgatása lefelé
                    new_key = (x, y + 1)
                    self.locked_positions[new_key] = self.locked_positions[key]
                    del self.locked_positions[key]
                elif y == line:
                    # Blokkok eltávolítása a törölt sorból
                    del self.locked_positions[key]
        
        # Rács frissítése
        self.update_grid()
        
        return len(lines_to_clear)
        
    def hard_drop(self):
        """Az elem azonnali leejtése a legalsó lehetséges pozícióba."""
        # Az elem lefelé mozgatása amíg lehet
        initial_y = self.current_piece.y
        while self.valid_move(self.current_piece, self.grid, 0, 1):
            self.current_piece.y += 1
        
        # Pontok hozzáadása az azonnali ejtésért (2 pont celláként)
        drop_points = HARD_DROP_POINTS * (self.current_piece.y - initial_y)
        self.score += drop_points
        
        # Elem rögzítése és új elem létrehozása
        self.lock_piece()
        self.fall_sound.play()
        
    def update_ghost_piece(self):
        """
        Frissíti a "szellem" elem pozícióját, amely megmutatja, hová fog esni az aktuális elem.
        
        Returns:
            Piece: A szellem elem
        """
        ghost_piece = self.current_piece.clone()
        
        # A szellem elem lefelé mozgatása amíg lehet
        while self.valid_move(ghost_piece, self.grid, 0, 1):
            ghost_piece.y += 1
        
        return ghost_piece if ghost_piece.y > self.current_piece.y else None
        
    def handle_input(self):
        """
        Felhasználói bemenet kezelése.
        
        Returns:
            bool: False ha a felhasználó kilépett, egyébként True
        """
        current_time = time.time() * 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # Billentyű lenyomás események
            if event.type == pygame.KEYDOWN:
                # Játékirányítás billentyűk
                if event.key == pygame.K_p:  # Szünet
                    self.paused = not self.paused
                
                if event.key == pygame.K_r:  # Újraindítás
                    self.reset_game()
                
                # Csak akkor kezeljük a mozgást, ha nincs szüneteltetve és nincs vége a játéknak
                if not self.paused and not self.game_over:
                    if event.key == pygame.K_LEFT:
                        if self.valid_move(self.current_piece, self.grid, -1, 0):
                            self.current_piece.move_left()
                            self.move_sound.play()
                        self.last_move_time[pygame.K_LEFT] = current_time
                        
                    elif event.key == pygame.K_RIGHT:
                        if self.valid_move(self.current_piece, self.grid, 1, 0):
                            self.current_piece.move_right()
                            self.move_sound.play()
                        self.last_move_time[pygame.K_RIGHT] = current_time
                        
                    elif event.key == pygame.K_DOWN:
                        self.down_pressed = True
                        self.last_move_time[pygame.K_DOWN] = current_time
                        
                    elif event.key == pygame.K_UP:  # Forgatás
                        # Aktuális forgatás mentése
                        old_rotation = self.current_piece.rotation
                        
                        # Forgatás
                        self.current_piece.rotate()
                        
                        # Ha a forgatás nem érvényes, próbáljunk fal-rúgásokat
                        if not self.valid_move(self.current_piece, self.grid):
                            # Próbáljunk jobbra mozgatni, ha balra blokkolva van
                            if self.valid_move(self.current_piece, self.grid, 1, 0):
                                self.current_piece.move_right()
                            # Próbáljunk balra mozgatni, ha jobbra blokkolva van
                            elif self.valid_move(self.current_piece, self.grid, -1, 0):
                                self.current_piece.move_left()
                            # Próbáljunk felfelé mozgatni, ha lent blokkolva van
                            elif self.valid_move(self.current_piece, self.grid, 0, -1):
                                self.current_piece.y -= 1
                            else:
                                # Ha minden sikertelen, visszaállítjuk a forgatást
                                self.current_piece.rotation = old_rotation
                        
                        if self.current_piece.rotation != old_rotation:
                            self.rotate_sound.play()
                        
                    elif event.key == pygame.K_SPACE:  # Azonnali ejtés
                        self.hard_drop()
            
            # Billentyű felengedés események
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.down_pressed = False
        
        # Lenyomva tartott billentyűk kezelése (folyamatos mozgás)
        keys = pygame.key.get_pressed()
        
        if not self.paused and not self.game_over:
            # Bal/jobb mozgás ismétlési késleltetéssel
            if keys[pygame.K_LEFT] and current_time - self.last_move_time[pygame.K_LEFT] > MOVE_REPEAT_DELAY:
                if self.valid_move(self.current_piece, self.grid, -1, 0):
                    self.current_piece.move_left()
                    self.last_move_time[pygame.K_LEFT] = current_time
            
            if keys[pygame.K_RIGHT] and current_time - self.last_move_time[pygame.K_RIGHT] > MOVE_REPEAT_DELAY:
                if self.valid_move(self.current_piece, self.grid, 1, 0):
                    self.current_piece.move_right()
                    self.last_move_time[pygame.K_RIGHT] = current_time
            
            # Gyors ejtés (gyorsabb esés amikor a le nyíl lenyomva van)
            if self.down_pressed and current_time - self.last_move_time[pygame.K_DOWN] > MOVE_REPEAT_DELAY / 2:
                if self.valid_move(self.current_piece, self.grid, 0, 1):
                    self.current_piece.move_down()
                    self.score += SOFT_DROP_POINTS  # Kis pontbónusz a gyors ejtésért
                    self.last_move_time[pygame.K_DOWN] = current_time
                    
        return True
    
    def update(self):
        """Játék állapot frissítése."""
        current_time = time.time() * 1000
        
        # Normál gravitációs ejtés, ha nincs szüneteltetve vagy vége a játéknak
        if not self.paused and not self.game_over:
            if current_time - self.last_drop_time > self.drop_speed:
                self.last_drop_time = current_time
                
                if self.valid_move(self.current_piece, self.grid, 0, 1):
                    self.current_piece.move_down()
                else:
                    self.lock_piece()
                
    def draw(self):
        """Játékállapot kirajzolása a képernyőre."""
        # Háttér rajzolása
        self.ui.draw_background()
        
        # Cím rajzolása
        self.ui.draw_title()
        
        # Játéktér háttér rajzolása
        self.screen.blit(self.ui.panel_main, (TOP_LEFT_X - 20, TOP_LEFT_Y - 20))
        
        # Rács, elemek és UI elemek rajzolása ha nincs vége a játéknak
        self.ui.draw_grid_blocks(self.grid)
        self.ui.draw_grid_lines()
        
        if not self.game_over:
            # Szellem elem rajzolása
            ghost_piece = self.update_ghost_piece()
            if ghost_piece:
                self.ui.draw_piece(ghost_piece, ghost=True)
                
            # Aktuális elem rajzolása
            self.ui.draw_piece(self.current_piece)
        
        # UI elemek rajzolása
        self.ui.draw_next_piece(self.next_piece)
        self.ui.draw_score(self.score, self.level, self.lines_cleared, self.combo, self.last_score_increase)
        self.ui.draw_controls()
        
        # Játék vége vagy szüneteltetés képernyő rajzolása, ha szükséges
        if self.game_over:
            self.ui.draw_game_over(self.score)
        elif self.paused:
            self.ui.draw_pause()
        
        # Képernyő frissítése
        pygame.display.update()
    
    def run(self):
        """Fő játék ciklus futtatása."""
        running = True
        
        while running:
            # Bemenet kezelése
            running = self.handle_input()
            
            # Játék frissítése
            self.update()
            
            # Játék kirajzolása
            self.draw()
            
            # Képkocka ráta korlátozása
            self.clock.tick(60)
        
        # Pygame leállítása, ha kész
        pygame.quit()