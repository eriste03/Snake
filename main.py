# Imports
from objects.board import Board
from objects.snake import Snake
from objects.apple import Apple
import pygame, sys, time

# MainWindow
class MainWindow:
    FRAMES_PER_SECOND = 50                                                      # Frames per second
    MOVES_PER_SECOND = {"EASY": 5, "MEDIUM": 8, "HARD": 12}                      # Snake moves per second

    def __init__(self):
        # Window properties
        pygame.init()                                                           # Initialize pygame
        self.screen = pygame.display.set_mode((800, 800))                       # Initialize window
        pygame.display.set_caption("Snake - Erik Steigen")                      # Update window title
        self.clock = pygame.time.Clock()                                        # Initialize clock for fps alignment
        self.eatingSound = pygame.mixer.Sound("sounds/food.mp3")
        self.crashSound = pygame.mixer.Sound("sounds/gameover.mp3")

        # Default settings
        self.difficulty = "MEDIUM"
        self.size = "SMALL"

        # Initialize game
        self.initialize()

    def initialize(self):
        """Display the setup screen"""
        font = pygame.font.Font(None, 36)

        # Button coordinates and settings
        self.buttons = {
            "DIFFICULTY": pygame.Rect(200, 80, 400, 50),
            "EASY": pygame.Rect(80, 150, 200, 100),
            "MEDIUM": pygame.Rect(300, 150, 200, 100),
            "HARD": pygame.Rect(520, 150, 200, 100),
            "SIZE": pygame.Rect(200, 330, 400, 50),
            "SMALL": pygame.Rect(80, 400, 200, 100),
            "MEDIUM_SIZE": pygame.Rect(300, 400, 200, 100),
            "LARGE": pygame.Rect(520, 400, 200, 100),
            "PLAY": pygame.Rect(300, 600, 200, 80)
        }

        while True:
            self.screen.fill((255, 255, 255))
            self.drawButtons(font)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handleClick(event.pos)
            
            pygame.display.flip()
            self.clock.tick(MainWindow.FRAMES_PER_SECOND)
    
    def drawButtons(self, font):
        
        # Difficulties
        pygame.draw.rect(self.screen, (0, 0, 0), self.buttons["DIFFICULTY"])
        text = font.render("CHOOSE DIFFICULTY:", True, (255, 255, 255))
        self.screen.blit(text, text.get_rect(center=self.buttons["DIFFICULTY"].center))
        for difficulty in ["EASY", "MEDIUM", "HARD"]:
            color = (0, 200, 0) if self.difficulty == difficulty else (200, 200, 200)
            pygame.draw.rect(self.screen, color, self.buttons[difficulty])
            text = font.render(difficulty, True, (0, 0, 0))
            self.screen.blit(text, text.get_rect(center=self.buttons[difficulty].center))
        
        # Sizes
        pygame.draw.rect(self.screen, (0, 0, 0), self.buttons["SIZE"])
        text = font.render("CHOOSE SIZE:", True, (255, 255, 255))
        self.screen.blit(text, text.get_rect(center=self.buttons["SIZE"].center))
        for size in ["SMALL", "MEDIUM_SIZE", "LARGE"]:
            sizeName = "MEDIUM" if size == "MEDIUM_SIZE" else size
            color = (0, 200, 0) if self.size == sizeName else (200, 200, 200)
            pygame.draw.rect(self.screen, color, self.buttons[size])
            text = font.render(sizeName, True, (0, 0, 0))
            self.screen.blit(text, text.get_rect(center=self.buttons[size].center))
        
        # Play-button
        pygame.draw.rect(self.screen, (0, 150, 0), self.buttons["PLAY"])
        text = font.render("Play!", True, (255, 255, 255))
        self.screen.blit(text, text.get_rect(center=self.buttons["PLAY"].center))
    
    def handleClick(self, pos):
        """Handle button clicks to set difficulty, size, and start game"""
        if self.buttons["PLAY"].collidepoint(pos):
            self.startGame()
        elif self.buttons["EASY"].collidepoint(pos):
            self.difficulty = "EASY"
        elif self.buttons["MEDIUM"].collidepoint(pos):
            self.difficulty = "MEDIUM"
        elif self.buttons["HARD"].collidepoint(pos):
            self.difficulty = "HARD"
        elif self.buttons["SMALL"].collidepoint(pos):
            self.size = "SMALL"
        elif self.buttons["MEDIUM_SIZE"].collidepoint(pos):
            self.size = "MEDIUM"
        elif self.buttons["LARGE"].collidepoint(pos):
            self.size = "LARGE"
    
    def startGame(self):
        """Start the game with selected settings"""
        self.board = Board(self.size)
        self.snake = Snake(self.board.snake)
        self.apple = Apple(self.board.apple, self.board.board)
        self.cellSize = 800 / self.board.size[0]
        # self.movesPerSecond = 1000 // MainWindow.MOVES_PER_SECOND[self.difficulty]
        self.lastMoveTime = pygame.time.get_ticks()
        self.alreadyMoved = False
        self.started = False
        self.run()

    def draw(self):
        """Draw the board, snake, and apple"""
        # Draw grid
        for row in range(self.board.size[0]):
            for col in range(self.board.size[1]):
                # Draw each cell
                cellRect = pygame.Rect(col*self.cellSize, row*self.cellSize, self.cellSize, self.cellSize)
                pygame.draw.rect(self.screen, (200, 200, 200), cellRect, 1)
        
        # Draw snake
        for segment in self.snake.pos:
            segmentRect = pygame.Rect((segment[0]-1)*self.cellSize, (segment[1]-1)*self.cellSize, self.cellSize, self.cellSize)
            pygame.draw.rect(self.screen, (0, 255, 0), segmentRect)

        # Draw apple
        appleRect = pygame.Rect((self.apple.pos[0]-1)*self.cellSize, (self.apple.pos[1]-1)*self.cellSize, self.cellSize, self.cellSize)
        pygame.draw.rect(self.screen, (255, 0, 0), appleRect)

    def run(self):
        """Gameloop"""
        while True:

            # Get current time and move if ready
            if self.started:
                currentTime = pygame.time.get_ticks()
                if currentTime - self.lastMoveTime >= self.movesPerSecond:
                    moveResult = self.snake.move(self.apple.pos, self.board.board)
                    if moveResult["Crashed"]:
                        self.started = False
                        pygame.mixer.Sound.play(self.crashSound)
                        time.sleep(3)
                        self.initialize()
                    if moveResult["Eating"]:
                        pygame.mixer.Sound.play(self.eatingSound)
                        self.apple.changePos(self.snake.pos)
                    self.lastMoveTime = currentTime
                    self.alreadyMoved = False

            # Get events
            for event in pygame.event.get():

                # On quit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # On keypress
                if event.type == pygame.KEYDOWN:
                    if not self.started:
                        self.movesPerSecond = 1000 // MainWindow.MOVES_PER_SECOND[self.difficulty]
                        self.started = True
                    if not self.alreadyMoved:
                        if self.snake.updateHeading(event.key):
                            self.alreadyMoved = True

            # Fill and update screen with given FPS
            self.screen.fill((255, 255, 255))
            self.draw()
            pygame.display.flip()
            self.clock.tick(MainWindow.FRAMES_PER_SECOND)


def main():
    """
    Generate game object
    """
    window = MainWindow()
    window.run()

if __name__ == "__main__":
    main()