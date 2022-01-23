import pygame
import constants as c

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

    def draw(self, surface, offset=(0, 0)):
        x = offset[0]
        y = offset[1]
        if self.scale < 1:
            self.draw_surface = pygame.transform.scale(self.surface, (int(self.surface.get_width() * self.scale), int(self.surface.get_height() * self.scale)))
        width = self.draw_surface.get_width()
        height = self.draw_surface.get_height()
        x0 = x - width//2
        y0 = y - height//2 - 15
        if (self.age < self.plop_time) and self.animation:
            y0 -= (self.plop_time - self.age) * self.plop_speed
            self.draw_surface.set_alpha((1 - (self.plop_time - self.age)/self.plop_time) * 255)
        else:
            if (not self.shook) and self.game and self.animation:
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


BIRD_TYPES = (Bird, TurtleDove, RockDove)
def bird_from_key(key):
    for bird in BIRD_TYPES:
        if bird.key == key:
            return bird
    return None