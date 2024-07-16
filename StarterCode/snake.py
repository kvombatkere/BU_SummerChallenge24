import pygame
from pygame.locals import *
from random import randrange
import time, sys


class Player:
    """Player

    The player object contains the internal state of the player,
    including location of its pieces, direction and length.
    """
    def __init__(self, length=3, windowWidth=20, windowHeight=15, blockSize=40):
        self.length = length
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.blockSize = blockSize
        self.direction = 0
        self._image = None

        # TODO: Compute the starting position of the snake.
        # You should place the snake in the middle of the screen facing right.
        # The snake is represented by a list of (x, y) positions,
        # with the first being the head and the last being the tail.
        self.snake = [(0, 1)]

    def grow(self):
        """Grow makes the snake one length larger"""
        # TODO: Append the tail of the snake to itself making it larger and update the length
        pass

    def set_direction(self, direction):
        """Sets the direction of the snake.
        The snake cannot make a 180-degree turn.

        Directions:
            0 - Right
            1 - Up
            2 - Left
            3 - Down
        """
        # TODO: Check that the snake will not make an 180 degree
        self.direction = direction

    def update(self):
        """Moves the entire snake one step towards its direction"""
        # TODO: Move each position coordinates to the next position
        pass

        # TODO: Move the head of the snake one step towards the direction it is facing.
        #       Make sure to loop around when reaching a wall.
        pass

    def draw(self, surface):
        """Draws the snake on the surface"""
        if self._image is None:
            self._image = pygame.image.load("assets/snake.png").convert()
        for x, y in self.snake:
            surface.blit(self._image, (x * self.blockSize, y * self.blockSize))

    def collision(self, other):
        """Detects if that position is inside the snake"""
        for position in self.snake:
            if position == other:
                return True
        return False

    def boop(self):
        """Detects if the snake collided with itself"""
        # TODO: Iterate over all positions except the head.
        #       Check if it coincides with the head of the snake
        return False

class Apple:
    """Apple

    When the Snake touches the Apple, it grows by one length
    and the Apple is relocated
    """
    def __init__(self, windowWidth=20, windowHeight=15, blockSize=40):
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.blockSize = blockSize
        self.position = (0, 0)
        self._image = None

    def generate(self, player):
        """Generates a new Apple in an empty position"""
        # TODO: Use randint to place the Apple in an empty location
        self.position = (0, 0)

    def draw(self, surface):
        """Draw the apple on the board"""
        if self._image is None:
            self._image = pygame.image.load("assets/apple.png").convert()
        surface.blit(self._image, (self.position[0] * self.blockSize, self.position[1] * self.blockSize))


class Game:
    """Game

    The game module is responsible for running the game.
    """
    def __init__(self, windowWidth=20, windowHeight=15, blockSize=40, speed=20):
        """This is the initializing function of the Model object

        windowWidth:  windowWidth of the board in tiles
        windowHeight: windowHeight of the board in tiles
        blockSize:    size of each tile
        speed:  number of iterations in each second
        """
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.blockSize = blockSize
        self.speed = speed
        self.player = Player(3, windowWidth=self.windowWidth, windowHeight=self.windowHeight, blockSize=self.blockSize)
        self.apple = Apple(windowWidth=self.windowWidth, windowHeight=self.windowHeight, blockSize=self.blockSize)
        self.score_text = None
        self._running = False

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth * self.blockSize, self.windowHeight * self.blockSize), pygame.HWSURFACE)
        pygame.display.set_caption('BU Summer Challenge Snake')
        self.apple.generate(self.player)
        self.score_text = pygame.font.SysFont('Times New Roman', 30)

        self._running = True

    def on_loop(self):
        self.player.update()
        if self.player.collision(self.apple.position):
            self.player.grow()
            self.apple.generate(self.player)
        if self.player.boop():
            self._running = False
            self.quit()
            exit(0)

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self.player.draw(self._display_surf)
        self.apple.draw(self._display_surf)
        score_surf = self.score_text.render(str(self.player.length - 3), False, (255, 255, 255))
        self._display_surf.blit(score_surf, (20, 10))
        pygame.display.flip()

    def quit(self):
        pygame.display.quit()
        pygame.quit()
        print("Score: {}".format(self.player.length - 3))
        sys.exit()


    def on_execute(self):
        self.on_init()

        while(self._running):
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if (keys[K_RIGHT]):
                self.player.set_direction(0)

            if (keys[K_UP]):
                self.player.set_direction(1)

            if (keys[K_LEFT]):
                self.player.set_direction(2)

            if (keys[K_DOWN]):
                self.player.set_direction(3)

            self.on_loop()
            self.on_render()

            if (keys[K_ESCAPE]):
                self.quit()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            time.sleep(1 / self.speed)
        self.quit()
        

if __name__ == '__main__':
    game = Game()
    game.on_execute()
