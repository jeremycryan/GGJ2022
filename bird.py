import pygame
import constants as c
from particle import AngerParticle
import random
import math
import time


class Bird:
    key = "PIGEON"
    name = "Pigeon"
    description = "No more than 2 in a row."
    bird_count = 1
    movable = True
    color = (200, 200, 200)
    plop_time = 0.1
    plop_speed = 500

    surface = None
    surface_path = "pigeon.png"

    def __init__(self, game=None, animation=True):
        self.age = 0
        self.shook = False
        self.game = game

        self.ouch_alpha = 0
        self.animation = animation

        self.most_recent_draw = (0, 0)
        self.draw_surface = self.surface

        self.load_surfaces()
        self.scale = 1.0

    def load_surfaces(self):
        if not self.surface:
            self.surface = pygame.image.load(c.image_path(self.surface_path)).convert()
            self.surface.set_colorkey((255, 0, 255))
            mask = pygame.mask.from_surface(self.surface)
            self.ouch_surf = mask.to_surface(setcolor=(255, 0, 0), unsetcolor=(0, 0, 0)).convert()
            self.ouch_surf.set_colorkey((0, 0, 0))
            self.draw_surface = self.surface.copy()

    def update(self, dt, events):
        self.age += dt
        self.ouch_alpha -= 500*dt
        pass

    def can_place(self, grid, x, y):
        for xpos in x - 1, x, x + 1:
            if xpos < 0 or xpos >= grid.width:
                continue
            for ypos in y - 1, y, y + 1:
                if ypos < 0 or ypos >= grid.height:
                    continue
                birds = grid.get_birds_at(xpos, ypos)
                if Seagull.key in [bird.key for bird in birds]:
                    return False
        return True

    def draw(self, surface, offset=(0, 0)):
        x = offset[0]
        y = offset[1]
        if self.scale < 1:
            self.draw_surface = pygame.transform.scale(self.surface, (int(self.surface.get_width() * self.scale), int(self.surface.get_height() * self.scale)))
        else:
            self.draw_surface = self.surface.copy()
        width = self.draw_surface.get_width()
        height = self.draw_surface.get_height()
        x0 = x - width//2
        y0 = y - height//2 - 15
        if (self.age < self.plop_time) and self.animation:
            y0 -= (self.plop_time - self.age) * self.plop_speed
            self.draw_surface.set_alpha((1 - (self.plop_time - self.age)/self.plop_time) * 255)
        else:
            if (not self.shook) and self.game and self.animation:
                self.game.place_bird_sound.play()
                self.shook = True
                self.game.shake(7)
            self.draw_surface.set_alpha(255)
        surface.blit(self.draw_surface, (x0, y0))
        self.most_recent_draw = (x, y)

        if self.ouch_alpha > 0:
            self.ouch_surf.set_alpha(self.ouch_alpha)
            surface.blit(self.ouch_surf, (x0, y0))

    def flash_red(self):
        self.ouch_alpha = 255
        self.game.shake(12)


class TurtleDove(Bird):
    color = 64, 200, 64
    key = "TURTLE"
    name = "Turtle dove"
    description = "Only counts as half a pigeon."
    bird_count = 0.5
    surface_path = "turtle_dove.png"


class RockDove(Bird):
    color = 128, 128, 128
    key = "ROCK"
    name = "Rock dove"
    description = "It's made of rocks."
    movable = False
    surface_path = "rock_dove.png"

class Seagull(Bird):
    key = "RAVEN"
    name = "Raven"
    description = "Likes to dance, but needs space."
    surface_path = "raven.png"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.anger_particles = []
        self.since_anger = 0
        self.angery = False
        self.since_flash = time.time()%1
        self.flash_color = (0, 0, 0)
        self.surface = self.surface.copy()

    def can_place(self, grid, x, y):
        if not super().can_place(grid, x, y):
            return False
        for xpos in x-1, x, x+1:
            if xpos < 0 or xpos >= grid.width:
                continue
            for ypos in y-1, y, y+1:
                if ypos < 0 or ypos >= grid.height:
                    continue
                if grid.get_birds_at(xpos, ypos):
                    return False
        return True

    def update(self, dt, events):
        super().update(dt, events)
        self.since_anger += dt
        self.since_flash += dt
        self.flash_color = (self.flash_color[0]*0.1**dt, self.flash_color[1]*0.1**dt, self.flash_color[2]*0.1**dt)
        if self.since_flash > 1.0:
            self.flash()
        if self.since_anger > 0.25:
            self.angery = True

    def flash(self):
        self.flash_color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255)])
        self.since_flash = 0
        if self.animation:
            self.surface = pygame.transform.flip(self.surface, True, False)
            self.ouch_surf = pygame.transform.flip(self.ouch_surf, True, False)

    def load_surfaces(self):
        super().load_surfaces()
        if not self.animation:
            self.surface_path = "raven_still.png"
            self.surface = pygame.image.load(c.image_path("raven_still.png"))
            self.surface.set_colorkey((255, 0, 255))

    def draw(self, surface, offset=(0, 0)):
        self.draw_electric_fence(surface, offset=offset)
        x = offset[0]
        y = offset[1] + 10 * math.cos(self.since_flash * 25) / (self.since_flash * 20 + 1) * self.animation
        super().draw(surface, offset=(x, y))

    def draw_electric_fence(self, surface, offset):
        if not self.animation:
            return
        points = [(x/10, -1) for x in range(-10, 10)] + \
            [(1, (y/10)) for y in range(-10, 10)] + \
            [(x/10, 1) for x in range(10, -10, -1)] + \
            [(-1, (y/10)) for y in range(10, -10, -1)]
        points = [(x*c.TILE_WIDTH, y*c.TILE_HEIGHT) for x, y in points]
        points = [(x * self.scale, y*self.scale) for (x, y) in points]
        points = [(x + c.TILE_WIDTH*1.5 + random.random() * 3, y + random.random()*3 + c.TILE_WIDTH*1.5) for x, y in points.copy()]
        crazy = [(x + random.random() * 10 - 5, y + random.random()*10 - 5) for x, y in points.copy()]

        fence_surf = pygame.Surface((c.TILE_WIDTH * 3, c.TILE_HEIGHT * 3)).convert()
        flash_surf = pygame.Surface((int(c.TILE_WIDTH * 2 * self.scale), int(c.TILE_HEIGHT * 2 * self.scale))).convert()
        flash_surf.fill(self.flash_color)
        fence_surf.fill((0, 0, 0))
        fence_surf.blit(flash_surf, (fence_surf.get_width()//2 - flash_surf.get_width()//2, fence_surf.get_height()//2 - flash_surf.get_height()//2))
        pygame.draw.polygon(fence_surf, (100, 0, 0), crazy, 3)
        pygame.draw.polygon(fence_surf, (100, 100, 100), points, 2)
        surface.blit(fence_surf, (offset[0] - fence_surf.get_width()//2, offset[1] - fence_surf.get_height()//2), special_flags=pygame.BLEND_ADD)


BIRD_TYPES = (Bird, TurtleDove, RockDove, Seagull)
def bird_from_key(key):
    for bird in BIRD_TYPES:
        if bird.key == key:
            return bird
    return None