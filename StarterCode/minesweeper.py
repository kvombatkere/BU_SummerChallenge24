import pygame
from pygame.locals import *
from random import randrange, sample
import time

class Board:
    """Board

    This object holds the board details
    """
    def __init__(self, windowWidth=40, windowHeight=30, blockSize=20, mines=50):
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.blockSize = blockSize
        self.pressed = [[False] * self.windowWidth for _ in range(self.windowHeight)]
        self.flagged = [[False] * self.windowWidth for _ in range(self.windowHeight)]
        self.mines = mines
        self.is_mine = [[False] * self.windowWidth for _ in range(self.windowHeight)]
        self.neighboring_mine_count = [[0] * self.windowWidth for _ in range(self.windowHeight)]
        self.colors = [
                ("White", (192, 192, 192)),
                ("Blue", (0, 0, 255)),
                ("Green", (0, 255, 0)),
                ("Red", (255, 0, 0)),
                ("Purple", (255, 0, 255)),
                ("Black", (64, 64, 64)),
                ("Maroon", (128, 0, 0)),
                ("Gray", (128, 128, 128)),
                ("Turquoise", (64,224,208))
        ]
        self.font = None
        self.flag_image = None
        self.mine_image = None
        self._bombed = False
        self.remaining = self.windowWidth * self.windowHeight - self.mines

    def create(self):
        self.font = pygame.font.SysFont("Times New Roman", 30)
        mine_count = 0
        candidates = sum([[(x, y) for x in range(self.windowWidth)] for y in range(self.windowHeight)], [])

        # TODO: Use sample() to select positions for the mines
        pass

        # TODO: For each square find the number of neighboring mines
        for x in range(self.windowWidth):
            for y in range(self.windowHeight):
                pass

    def draw(self, surface):
        # TODO: For each cell if it is clicked print the number of neighboring mines in the appropriate color.
        #       If there are no adjoined mines paint the square grey.
        #       If the cell is flagged show the flag image.
        #       If the player has already clicked on a mine show all mines.
        for x in range(self.windowWidth):
            for y in range(self.windowHeight):
                pass

        for x in range(self.windowWidth - 1):
            pygame.draw.rect(surface, (255, 255, 255), ((x + 1) * self.blockSize, 0, 2, self.windowHeight * self.blockSize))
        for y in range(self.windowHeight - 1):
            pygame.draw.rect(surface, (255, 255, 255), (0, (y + 1) * self.blockSize, self.windowWidth * self.blockSize, 2))

    def click(self, x, y):
        # TODO: Check that the square is not clicked or flagged and the player
        #       has not stepped on a mine already.
        #       If the clicked square is has no adjacent mines, reveal all the adjoining ones
        return

    def flag(self, x, y):
        # TODO: When the player hits right click you need to flag or unflag the appropriate square
        #       Make sure you do not flag pressed squares or after the player has lost
        return

    def has_won(self):
        return self.remaining == 0


class Game:
    """Game

    The game module is responsible for running the game.
    """
    def __init__(self, windowWidth=20, windowHeight=15, blockSize=40, mines=40):
        """This is the initializing function of the Model object

        windowWidth:  windowWidth of the board in tiles
        windowHeight: windowHeight of the board in tiles
        blockSize:    size of each tile
        speed:  number of iterations in each second
        """
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.blockSize = blockSize
        self.board = Board(self.windowWidth, self.windowHeight, self.blockSize, mines)
        self._running = False

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth * self.blockSize, self.windowHeight * self.blockSize), pygame.HWSURFACE)
        pygame.display.set_caption('BU Summer Challenge Snake')
        self.board.create()

        self._running = True

    def on_loop(self):
        pass

    def on_render(self):
        self._display_surf.fill((0, 128, 255))
        self.board.draw(self._display_surf)
        pygame.display.flip()

    def win(self):
        text = pygame.font.SysFont('Times New Roman', 50)
        text_surf = text.render("Y O U   W I N !", True, (255, 0, 0), (0, 128, 255))
        self._display_surf.blit(text_surf, (self.windowWidth * self.blockSize / 2 - 150, self.windowHeight * self.blockSize/ 2 - 50))
        pygame.display.flip()
        self._running = False

    def quit(self):
        pygame.quit()

    def on_execute(self):
        self.on_init()

        while(True):
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if self._running:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.MOUSEBUTTONUP:
                        x, y = pygame.mouse.get_pos()
                        x, y = x // self.blockSize, y // self.blockSize
                        if event.button == 1:       # Left click
                            self.board.click(x, y)
                        if event.button == 3:       # right click
                            self.board.flag(x, y)

                    if event.type == pygame.QUIT:
                        self.quit()

                self.on_render()
                self.on_loop()

                if self.board.has_won():
                    self.win()

            if (keys[K_ESCAPE]):
                self.quit()
                return

            time.sleep(1 / 20)
        self.quit()


if __name__ == '__main__':
    game = Game()
    game.on_execute()
