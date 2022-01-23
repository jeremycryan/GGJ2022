import pygame
import constants as c
import math
import time


class TitleScene:

    def __init__(self, game, *args):
        self.game = game
        self.done = False

        self.p = pygame.image.load(c.image_path("p.png"))
        self.i = pygame.image.load(c.image_path("i.png"))
        self.g = pygame.image.load(c.image_path("g.png"))
        self.e = pygame.image.load(c.image_path("e.png"))
        self.o = pygame.image.load(c.image_path("o.png"))
        self.n = pygame.image.load(c.image_path("n.png"))
        self.hle = pygame.image.load(c.image_path("hle.png"))
        self.pidge = pygame.image.load(c.image_path("pigeon.png"))
        self.pidge = pygame.transform.scale2x(self.pidge).convert()
        self.pidge.set_colorkey((255, 0, 255))
        self.shadow = pygame.Surface((125, 60))
        self.shadow.fill((255, 255, 255))
        pygame.draw.ellipse(self.shadow, (200, 200, 200), self.shadow.get_rect())
        self.letters = [self.p, self.i, self.g, self.e, self.o, self.n]
        self.pac = pygame.image.load(c.image_path("pac.png"))
        self.level_path = ""

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.done = True
        pass

    def draw(self, surface, _offset=(0, 0)):
        self.draw_lines(surface)
        xoff = -75
        yoff = -30
        poses = [
            (xoff + 278, 205 + yoff),
            (xoff + 425, 200 + yoff),
            (xoff + 490, 215 + yoff),
            (xoff + c.WINDOW_WIDTH//2, 200 + yoff),
            (xoff + c.WINDOW_WIDTH//2 + 130, 190 + yoff),
            (xoff + c.WINDOW_WIDTH//2 + 295, 200 + yoff),
        ]
        for i, letter in enumerate(self.letters):
            pose = list(poses[i])
            pose[0] += 4 * math.cos((time.time() + i)*2)
            pose[1] += 4 * math.sin((time.time() + i/2)*2)
            surface.blit(letter, pose)
        surface.blit(self.hle, (c.WINDOW_WIDTH//2 - self.hle.get_width()//2, c.WINDOW_HEIGHT - self.hle.get_height() - 150), special_flags=pygame.BLEND_ADD)
        surface.blit(self.shadow, (545, 520), special_flags=pygame.BLEND_MULT)
        surface.blit(self.pidge, (540, 370))

        if time.time()%1 < 0.8:
            surface.blit(self.pac, (c.WINDOW_WIDTH//2 - self.pac.get_width()//2 - 10, c.WINDOW_HEIGHT - self.pac.get_height() - 10))


    def draw_lines(self, surface, _offset=(0, 0)):
        self.game.screen.fill((100, 10, 120))
        slope = 1.5
        period = 30
        start_x = 0 - surface.get_height()/slope + time.time()*0.6 % 1 * period
        color = (85, 3, 100)
        while start_x < surface.get_width():
            pygame.draw.line(surface, color, (start_x, surface.get_height()), (start_x + surface.get_height()/slope, 0), 2)
            start_x += period
