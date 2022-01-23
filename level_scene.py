from grid import Grid
import constants as c
import random
from bird import *
from inventory import Inventory
import yaml
import time
from principal import Principal


class LevelScene:

    def __init__(self, game, level_path):
        self.game = game
        self.level_path = level_path
        self.inventory = Inventory(self)
        self.rocks = []
        self.principal = None
        self.done = False
        self.next_level = None
        self.camera_x = -c.WINDOW_WIDTH
        self.level_finished = False

        self.grid = self.load_grid()


    def load_grid(self):
        with open(c.level_path(self.level_path), "r") as f:
            data = yaml.load(f, yaml.Loader)
        grid = Grid(data["width"], data["height"], self)
        self.inventory.set_starting_birds(data["inventory"])
        if "principal" in data:
            self.principal = Principal(data["principal"])
            if self.game.seen_rocks and self.level_path in ["circle_4x4.yaml", "fish_4x4.yaml", "hourglass_4x4.yaml", "stairs_4x4.yaml"]:
                self.principal = None
        if "rocks" in data:
            self.rocks = data["rocks"]
            self.game.seen_rocks = True
        return grid

    def draw_lines(self, surface, _offset=(0, 0)):
        slope = 1.5
        period = 30
        start_x = 0 - surface.get_height()/slope + time.time()*0.6 % 1 * period
        color = (85, 3, 100)
        while start_x < surface.get_width():
            pygame.draw.line(surface, color, (start_x, surface.get_height()), (start_x + surface.get_height()/slope, 0), 2)
            start_x += period

    def complete(self):
        self.level_finished = True

    def update(self, dt, events):
        conditional_events = events
        if self.principal and not self.principal.done:
            conditional_events = ()
        self.inventory.update(dt, conditional_events)
        self.grid.update(dt, conditional_events)

        if self.principal:
            self.principal.update(dt, events)

        if not self.level_finished:
            self.camera_x *= 0.003**dt
            self.camera_x += 70*dt
            self.camera_x = min(self.camera_x, 0)
        else:
            self.camera_x -= 1000*dt
            self.camera_x *= 100**dt
            self.inventory.submit_button.y += 10*dt
            self.inventory.submit_button.y *= 2**dt
            if self.camera_x <= -c.WINDOW_WIDTH:
                self.done = True

        if self.camera_x > -5 and not self.grid.controls_enabled:
            self.grid.controls_enabled = True
            for rock in self.rocks:
                self.grid.add_bird(rock[0], rock[1], RockDove(self.game))

    def draw(self, surface, offset=(0, 0)):
        self.game.screen.fill((100, 10, 120))
        self.draw_lines(surface)
        x = offset[0] + c.LEVEL_RECTANGLE_CENTER[0]
        y = offset[1] + c.LEVEL_RECTANGLE_CENTER[1]
        self.grid.draw(surface, offset=(x + self.camera_x, y))
        self.inventory.draw(surface, offset=(offset[0] + self.camera_x, offset[1]))

        if self.principal:
            self.principal.draw(surface, offset=offset)
