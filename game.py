import pygame
import sys
import math


import constants as c
from level_scene import LevelScene
from title_scene import TitleScene


class Game:

    def __init__(self):
        pygame.init()

        self.music = pygame.mixer.Sound(c.sound_path("birdsong.ogg"))
        self.music.set_volume(0.7)
        self.music.play(-1)
        self.place_bird_sound = pygame.mixer.Sound(c.sound_path("place_bird.wav"))
        self.place_bird_sound.set_volume(0.1)
        self.pick_up_bird_sound = pygame.mixer.Sound(c.sound_path("pick_up_bird.wav"))
        self.pick_up_bird_sound.set_volume(0.13)
        self.talk_sound = pygame.mixer.Sound(c.sound_path("pigeonhole_talk.wav"))
        self.talk_sound.set_volume(0.02)
        self.advance_dialogue_noise = pygame.mixer.Sound(c.sound_path("advance_dialog.wav"))
        self.advance_dialogue_noise.set_volume(0.1)
        self.try_again_noise = pygame.mixer.Sound(c.sound_path("try_again.wav"))
        self.try_again_noise.set_volume(0.1)
        self.change_bird_type = pygame.mixer.Sound(c.sound_path("change_bird_type.wav"))
        self.change_bird_type.set_volume(0.04)
        self.victory_sound = pygame.mixer.Sound(c.sound_path("victory.wav"))
        self.victory_sound.set_volume(0.2)

        self.screen = pygame.display.set_mode(c.WINDOW_SIZE)
        pygame.display.set_caption(c.TITLE)
        self.clock = pygame.time.Clock()

        self.since_shake = 0
        self.shake_amt = 0
        self.seen_rocks = False

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
        levels = [
            "basic_2x2.yaml",
            "basic_3x3.yaml",
            "basic_4x4.yaml",
            "stairs_4x4.yaml",
            "circle_4x4.yaml",
            "hourglass_4x4.yaml",
            "fish_4x4.yaml",
            "turtles_3x3.yaml",
            "turtles_4x4.yaml",
            "turtles_5x5.yaml",
            "basic_5x5.yaml",
            "raven_5x5.yaml",
            "raven_6x6.yaml",
            "basic_6x6.yaml",

            "test_level.yaml",
        ]
        self.level = TitleScene(self)
        while True:
            dt = self.clock.tick(c.FPS)/1000
            dt, events = self.get_events(dt)

            self.level.update(dt, events)
            self.level.draw(self.screen, self.get_shake_offset())

            if self.level.done:
                if self.level.level_path == "basic_4x4.yaml":
                    solved = self.level.grid.get_4x4_type()
                    if solved and solved in levels:
                        levels.remove(solved)

                self.level = LevelScene(self, levels.pop(0))

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