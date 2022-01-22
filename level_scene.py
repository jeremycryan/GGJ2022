from grid import Grid
import constants as c
import random
from bird import *


class LevelScene:

    def __init__(self, game):
        self.game = game
        self.starting_birds = ()
        self.grid = self.load_grid()
        self.done = False
        self.next_level = None

    def load_grid(self):
        grid = Grid(8,8, self)
        self.starting_birds = [Bird()] * 6
        # for cell in grid.enumerate_cells():
        #     if random.random() < 0.5: cell.add_bird(random.choice([Bird(), TurtleDove(), RockDove()]))
        return grid

    def complete(self):
        self.next_level = LevelScene
        self.done = True

    def update(self, dt, events):
        self.grid.update(dt, events)

    def draw(self, surface, offset=(0, 0)):
        x = offset[0] + c.LEVEL_RECTANGLE_CENTER[0]
        y = offset[1] + c.LEVEL_RECTANGLE_CENTER[1]
        self.grid.draw(surface, offset=(x, y))
