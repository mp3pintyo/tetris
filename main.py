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