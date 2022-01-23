import pygame

import constants as c


class Principal:
    def __init__(self, lines, game):
        self.lines = lines
        self.current_line = 0
        self.time_on_current_line = 0
        self.game = game
        self.age = 0

        self.gradient = pygame.image.load(c.image_path("gradient_2.png"))
        self.gradient = pygame.transform.scale(self.gradient, (c.WINDOW_WIDTH, self.gradient.get_height()))

        self.label = pygame.image.load(c.image_path("pigeonhole_label.png"))

        self.principal = pygame.image.load(c.image_path("principal_pigeonhole.png"))

        self.font = pygame.font.Font(c.font_path("micross.ttf"), 20)
        self.done = False

        self.since_tweet = 0
        self.at = 1


    def update(self, dt, events):
        self.age += dt
        if self.age < self.at:
            return
        self.since_tweet += dt
        if self.lines and int(self.time_on_current_line * c.CHARS_PER_SECOND) < len(self.lines[self.current_line]):
            if self. since_tweet > 0.12:
                self.game.talk_sound.play()
                self.since_tweet -= 0.12

        self.time_on_current_line += dt

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not self.done and self.time_on_current_line * c.CHARS_PER_SECOND > len(self.lines[self.current_line]):
                        self.time_on_current_line = 0
                        if len(self.lines) > 1:
                            self.since_tweet = 0
                            self.lines.pop(0)
                        else:
                            self.lines = []
                            self.done = True
                        self.game.advance_dialogue_noise.play()

    def draw(self, surface, offset=(0, 0)):
        yoff = self.done * (self.time_on_current_line**2 * 2500 - self.time_on_current_line * 300)
        pxoff = (self.time_on_current_line * 400) * self.done
        pyoff = (self.time_on_current_line**2 * 2400 - self.time_on_current_line * 1200) * self.done
        pspin = self.done * self.time_on_current_line * 600


        if self.age < self.at:
            youngness = (1 - self.age/self.at)
            yoff = 300 * youngness**2
            pxoff = -300 * youngness**2
            pyoff = -300 * youngness**2
            pspin = 60 * youngness**2

        psurf = self.principal.copy()
        psurf = pygame.transform.rotate(psurf, pspin)


        surface.blit(self.gradient, (0, c.WINDOW_HEIGHT - self.gradient.get_height() + 50 + yoff), special_flags=pygame.BLEND_MULT)
        surface.blit(self.label, (-50 -yoff * 3, c.WINDOW_HEIGHT - 200), special_flags=pygame.BLEND_ADD)
        surface.blit(psurf, (105 + pxoff - psurf.get_width()//2, c.WINDOW_HEIGHT - 235 + pyoff - psurf.get_height()//2))

        chars_to_show = int(self.time_on_current_line * c.CHARS_PER_SECOND)

        if self.lines:
            lines = self.lines[self.current_line][:chars_to_show].split("\n")
        else:
            lines = []

        x = 200
        y = c.WINDOW_HEIGHT - 120
        for line in lines:
            surf = self.font.render(line, 0, (200, 160, 220))
            surface.blit(surf, (x, y))
            y += 24

        pass