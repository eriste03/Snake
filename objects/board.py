class Board:
    SIZE = {                    # Sizes and positions on the board
        "SMALL": {                  # Small board
            "SIZE": (10, 10),            # Board size (x, y)
            "SNAKE": (3, 5),            # Snake startPos (x, y)
            "APPLE": (8, 5)},           # Apple startPos (x, y)
        "MEDIUM": {                 # Medium board
            "SIZE": (16, 16),           # Board size (x, y)
            "SNAKE": (4, 8),            # Snake startPos (x, y)
            "APPLE": (13, 8)},          # Apple startPos (x, y)
        "LARGE": {                  # Large board
            "SIZE": (25, 25),           # Board size (x, y)
            "SNAKE": (6, 12),           # Snake startPos (x, y)
            "APPLE": (19, 12)}}         # Apple startPos (x, y)
    
    def __init__(self, size):
        self.size = Board.SIZE[size]["SIZE"]                                                # Initialize board-size from given argument "size"
        self.snake = [Board.SIZE[size]["SNAKE"]]                                            # Initialize snake-startPos
        self.apple = Board.SIZE[size]["APPLE"]                                              # Initialize apple-startPos
        self.board = [(x+1, y+1) for x in range(self.size[0]) for y in range(self.size[1])] # Generate board

if __name__ == "__main__":
    oBoard1 = Board("SMALL")
    print(f"Size   {len(oBoard1.board)}\nBoard  {oBoard1.size}\nApple  {oBoard1.apple}\nSnake  {oBoard1.snake}\n")
    oBoard2 = Board("MEDIUM")
    print(f"Size   {len(oBoard2.board)}\nBoard  {oBoard2.size}\nApple  {oBoard2.apple}\nSnake  {oBoard2.snake}\n")
    oBoard3 = Board("LARGE")
    print(f"Size   {len(oBoard3.board)}\nBoard  {oBoard3.size}\nApple  {oBoard3.apple}\nSnake  {oBoard3.snake}")