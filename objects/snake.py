import pygame

class Snake:
    
    def __init__(self, startPos):
        self.pos = startPos         # Current pos of snake (): list[int]
        self.heading = "east"       # Heading: "north", "east", "south", or "west"
        self.eating = False         # Currently eating in given coordinate

    def updateHeading(self, key):
        # Move up
        if key in [pygame.K_UP, pygame.K_w] and self.heading != "north" and self.heading != "south":
            self.heading = "north"
        # Move right
        elif key in [pygame.K_RIGHT, pygame.K_d] and self.heading != "east" and self.heading != "west":
            self.heading = "east"
        # Move down
        elif key in [pygame.K_DOWN, pygame.K_s] and self.heading != "south" and self.heading != "north":
            self.heading = "south"
        # Move left
        elif key in [pygame.K_LEFT, pygame.K_a] and self.heading != "west" and self.heading != "east":
            self.heading = "west"
        # No movement
        else:
            return False
        print(f"New heading: {self.heading}")
        return True
        
    def move(self, applePos, boardList):
        # Initialize list for returns
        returnList = {"Crashed": False, "Eating": False}

        # Add new position for head
        if self.heading == "north":     # x, y-1
            self.pos.append((self.pos[-1][0], self.pos[-1][1]-1))
        elif self.heading == "east":    # x+1, y
            self.pos.append((self.pos[-1][0]+1, self.pos[-1][1]))
        elif self.heading == "south":   # x, y+1
            self.pos.append((self.pos[-1][0], self.pos[-1][1]+1))
        elif self.heading == "west":    # x-1, y
            self.pos.append((self.pos[-1][0]-1, self.pos[-1][1]))

        # If snake did not eat and should stay same length
        if not self.eating:
            self.pos = self.pos[1:]

        # If snake crashed into wall
        if self.pos[-1] not in boardList:
            print("Crashed into wall")
            returnList["Crashed"] = True
        
        # If snake crashed into self
        elif self.pos[-1] in self.pos[:-1]:
            print("Crashed into self")
            returnList["Crashed"] = True

        # If snake is eating apple after position has been changed
        if self.pos[-1] == applePos:
            print("Apple maltracted")
            self.eating = True
            returnList["Eating"] = True
        else:
            self.eating = False

        # Return
        return returnList