import pygame
import constants as c


class Bird:
    key = "PIGEON"
    bird_count = 1
    movable = True
    color = (200, 200, 200)
    plop_time = 0.1
    plop_speed = 500

    surface = None

    def __init__(self, game=None):
        self.age = 0
        self.shook = False
        self.game = game

        self.ouch_alpha = 0

        self.load_surfaces()

    @classmethod
    def load_surfaces(cls):
        if not cls.surface:
            cls.surface = pygame.image.load(c.image_path("pigeon.png")).convert()
            cls.surface.set_colorkey((255, 0, 255))
            mask = pygame.mask.from_surface(cls.surface)
            cls.ouch_surf = mask.to_surface(setcolor=(255, 0, 0), unsetcolor=(0, 0, 0)).convert()
            cls.ouch_surf.set_colorkey((0, 0, 0))

    def update(self, dt, events):
        self.age += dt
        self.ouch_alpha -= 500*dt
        pass

    def draw(self, surface, offset=(0, 0)):
        x = offset[0]
        y = offset[1]
        width = self.surface.get_width()
        height = self.surface.get_height()
        x0 = x - width//2
        y0 = y - height//2 - 15
        if self.age < self.plop_time:
            y0 -= (self.plop_time - self.age) * self.plop_speed
            self.surface.set_alpha((1 - (self.plop_time - self.age)/self.plop_time) * 255)
        else:
            if (not self.shook) and self.game:
                self.shook = True
                self.game.shake(7)
            self.surface.set_alpha(255)
        surface.blit(self.surface, (x0, y0))

        if self.ouch_alpha > 0:
            self.ouch_surf.set_alpha(self.ouch_alpha)
            surface.blit(self.ouch_surf, (x0, y0))

    def flash_red(self):
        self.ouch_alpha = 255
        self.game.shake(12)


class TurtleDove(Bird):
    color = 64, 200, 64
    key = "TURTLE"
    bird_count = 0.5


class RockDove(Bird):
    color = 128, 128, 128
    key = "ROCK"
    movable = False


