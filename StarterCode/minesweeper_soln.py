import sys
import pygame
from pygame.locals import *
from random import sample
import time


class Board:
    """Board
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
            ("Turquoise", (64, 224, 208))
        ]
        self.font = None
        self.flag_image = pygame.image.load('assets/flag.png')

        self.mine_image = pygame.image.load('assets/mine.jpeg')
        self._bombed = False
        self.remaining = self.windowWidth * self.windowHeight - self.mines

    def create(self):
        self.font = pygame.font.SysFont("Times New Roman", 30)
        mine_count = 0
        candidates = sum([[(x, y) for x in range(self.windowWidth)] for y in range(self.windowHeight)], [])
        # TODO: Use sample() to select positions for the mines
        ##DONE
        self.mine_placement = sample(candidates, self.mines)
        for x,y in self.mine_placement:
            self.is_mine[y][x] = True
        # TODO: For each square find the number of neighboring mines
        ##DONE
        for x in range(self.windowWidth):
            for y in range(self.windowHeight):
                if self.is_mine[y][x]:
                    for new_x, new_y in [(x + 1, y), (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y), (x - 1, y - 1),
                                     (x, y - 1), (x + 1, y - 1)]:
                        if(0<=new_x<self.windowWidth) and (0<=new_y<self.windowHeight):
                            self.neighboring_mine_count[new_y][new_x]+=1

        print(self.neighboring_mine_count)
        print(self.mine_placement)
    def draw(self, surface):
        # TODO: For each cell if it is clicked print the number of neighboring mines in the appropriate color.
        #       If there are no adjoined mines paint the square grey.
        #       If the cell is flagged show the flag image.
        #       If the player has already clicked on a mine show all mines.
        ##DONE
        for x in range(self.windowWidth):
            for y in range(self.windowHeight):
                if self.pressed[y][x]:
                    pygame.draw.rect(surface, (128, 128, 128),
                                     (x * self.blockSize, y * self.blockSize, self.blockSize, self.blockSize))
                    if self.neighboring_mine_count[y][x] > 0:
                        pygame.draw.rect(surface, (0, 0, 255),
                                         (x * self.blockSize, y * self.blockSize, self.blockSize, self.blockSize))
                        Font1 = pygame.font.SysFont('monaco', 45)
                        numSurf = Font1.render('{0}'.format(self.neighboring_mine_count[y][x]), True, (255, 0, 0))
                        numRect = numSurf.get_rect()
                        numRect.topleft = (x*self.blockSize+5, y*self.blockSize+5)
                        surface.blit(numSurf,numRect)
                if self.flagged[y][x] and not self._bombed:
                    surface.blit(self.flag_image, (x*self.blockSize, y*self.blockSize))
                if self.is_mine[y][x] and self._bombed:
                    surface.blit(self.mine_image, (x*self.blockSize, y*self.blockSize))
                    self.lose(surface)
        for x in range(self.windowWidth - 1):
            pygame.draw.rect(surface, (255, 255, 255),
                             ((x + 1) * self.blockSize, 0, 2, self.windowHeight * self.blockSize))
        for y in range(self.windowHeight - 1):
            pygame.draw.rect(surface, (255, 255, 255),
                             (0, (y + 1) * self.blockSize, self.windowWidth * self.blockSize, 2))
    
    def lose(self, surface):
        loseFont = pygame.font.SysFont('monaco', 60)
        loseSurf = loseFont.render('Y O U  L O S E!', True, (0, 255, 0))
        loseRect = loseSurf.get_rect()
        loseRect.midtop = (self.windowWidth*self.blockSize/2, 80)
        surface.blit(loseSurf, loseRect)
    
    def click(self, x, y):
        # TODO: Check that the square is not clicked or flagged and the player
        #       has not stepped on a mine already.
        #       If the clicked square is has no adjacent mines, reveal all the adjoining ones
        ##DONE
        if self._bombed or self.pressed[y][x] or self.flagged[y][x]:
            return
        if self.is_mine[y][x]:
            self._bombed = True
        else:
            self.pressed[y][x] = True
            self.remaining = self.remaining - 1
            if self.neighboring_mine_count[y][x] == 0:
                for new_x, new_y in [(x + 1, y), (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y), (x - 1, y - 1),
                                     (x, y - 1), (x + 1, y - 1)]:
                    if (0 <= new_x < self.windowWidth) and (0 <= new_y < self.windowHeight):
                        self.click(new_x, new_y)

    def flag(self, x, y):
        # TODO: Check that the square is pressed with the right click and switch the flag value for that square
        ##DONE
        if(self.flagged[y][x]):
            self.flagged[y][x] = False
        else:
            self.flagged[y][x] = True

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
        self._display_surf = pygame.display.set_mode(
            (self.windowWidth * self.blockSize, self.windowHeight * self.blockSize), pygame.HWSURFACE)
        pygame.display.set_caption('BU Summer Challenge Minesweeper')
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
        self._display_surf.blit(text_surf, (
        self.windowWidth * self.blockSize / 2 - 150, self.windowHeight * self.blockSize / 2 - 50))
        pygame.display.flip()
        self._running = False

    def quit(self):
        pygame.quit()

    def on_execute(self):
        self.on_init()

        while (True):
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if self._running:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.MOUSEBUTTONUP:
                        x, y = pygame.mouse.get_pos()
                        x, y = x // self.blockSize, y // self.blockSize
                        if event.button == 1:  # Left click
                            self.board.click(x, y)
                        if event.button == 3:  # right click
                            self.board.flag(x, y)

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