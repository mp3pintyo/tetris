from config import SHAPE_COLORS, SHAPES

class Piece:
    """
    A Tetris játék egy elemét reprezentáló osztály.
    Kezeli az elem tulajdonságait és mozgását.
    """
    def __init__(self, x, y, shape_index):
        """
        Inicializálja az elemet.
        
        Args:
            x (int): X pozíció a játéktérben (0-9)
            y (int): Y pozíció a játéktérben (kezdeti érték általában 0)
            shape_index (int): Alakzat indexe a SHAPES listában
        """
        self.x = x
        self.y = y
        self.shape_index = shape_index
        self.color = SHAPE_COLORS[shape_index]
        self.rotation = 0
        self.shape = SHAPES[shape_index]

    def get_shape(self):
        """
        Visszaadja az elem aktuális alakzatát a forgatás figyelembevételével.
        
        Returns:
            list: Az aktuális alakzat mátrixa
        """
        return self.shape[self.rotation % len(self.shape)]

    def rotate(self):
        """
        Elforgatja az elemet az óramutató járásával megegyezően.
        """
        self.rotation += 1
        if self.rotation >= len(self.shape):
            self.rotation = 0
    
    def rotate_back(self):
        """
        Visszaforgatja az elemet (óramutató járásával ellentétesen).
        Használható például ha egy forgatás érvénytelen pozícióba vinné az elemet.
        """
        self.rotation -= 1
        if self.rotation < 0:
            self.rotation = len(self.shape) - 1
            
    def move_left(self):
        """Az elemet balra mozgatja egy cellával."""
        self.x -= 1
        
    def move_right(self):
        """Az elemet jobbra mozgatja egy cellával."""
        self.x += 1
        
    def move_down(self):
        """Az elemet lefelé mozgatja egy cellával."""
        self.y += 1
        
    def clone(self):
        """
        Az elem másolatát készíti el.
        Hasznos például előnézet készítéséhez.
        
        Returns:
            Piece: Az elem másolata
        """
        piece = Piece(self.x, self.y, self.shape_index)
        piece.rotation = self.rotation
        return piece