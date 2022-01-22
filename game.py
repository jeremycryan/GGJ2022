import pygame
import sys
import math


import constants as c
from level_scene import LevelScene


class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(c.WINDOW_SIZE)
        pygame.display.set_caption(c.TITLE)
        self.clock = pygame.time.Clock()

        self.since_shake = 0
        self.shake_amt = 0

        self.main()

    def shake(self, amt=15):
        self.shake_amt = max(amt, self.shake_amt)
        self.since_shake = 0

    def get_shake_offset(self):
        xoff = math.cos(self.since_shake*40) * self.shake_amt
        yoff = math.sin(self.since_shake*25) * self.shake_amt
        return (xoff, yoff)

    def main(self):
        self.clock.tick(c.FPS)
        level = LevelScene(self)
        while True:
            self.screen.fill((113, 20, 147))
            dt = self.clock.tick(c.FPS)/1000
            dt, events = self.get_events(dt)

            level.update(dt, events)
            level.draw(self.screen, self.get_shake_offset())

            if level.done:
                level = level.next_level(self)

            pygame.display.flip()



    def get_events(self, dt):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.since_shake += dt
        self.shake_amt *= 0.005**dt
        self.shake_amt -= 10*dt
        self.shake_amt = max(0, self.shake_amt)
        return dt, events


if __name__=="__main__":
    Game()