import random

class Apple:
    def __init__(self, startPos, boardList):
        self.pos = startPos
        self.board = boardList

    def changePos(self, snakePos):
        random.shuffle(self.board)
        for pos in self.board:
            if pos not in snakePos:
                self.pos = pos
                print(f"New apple pos: {pos}")
                return