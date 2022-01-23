import pygame
import time
import random
import math
import constants as c

class Particle:
    color = (255, 255, 255)
    radius = 5

    def __init__(self, position, velocity=(0, 0), duration=5.0):
        self.duration = duration
        self.age = 0
        self.destroyed = False
        self.x, self.y = position
        self.vx, self.vy = velocity

    def update(self, dt, events):
        if self.destroyed:
            return
        self.age += dt
        if self.through() >= 1:
            self.destroyed = True
        self.x += self.vx*dt
        self.y += self.vy*dt
        pass

    def through(self):
        if self.age > self.duration:
            return 1
        return self.age/self.duration

    def draw(self, surface, offset=(0, 0)):
        if self.destroyed:
            return
        x = self.x + offset[0]
        y = self.y + offset[1]
        pygame.draw.circle(surface, self.color, (x, y), self.radius)


class PigeonPlaceParticle(Particle):
    def __init__(self, position):
        duration = random.random() * 0.5 + 0.5
        self.starting_radius = 5 + 5*random.random()
        velocity_amt = random.random() * 32 + 75
        velocity_angle = random.random() * 360
        vx = velocity_amt * math.cos(velocity_angle)
        vy = velocity_amt * math.sin(velocity_angle)
        x, y = position
        x += math.cos(velocity_angle) * c.TILE_WIDTH//2
        y += math.sin(velocity_angle) * c.TILE_HEIGHT//2
        super().__init__(position=(x, y), velocity=(vx, vy), duration=duration)
        self.age = -0.1

    def update(self, dt, events):
        self.radius = self.starting_radius * (1 - (self.through())**2)
        self.vx *= 0.05**dt
        self.vy *= 0.05**dt
        self.color = (200 - 64*self.through(),)*3
        super().update(dt, events)

    def draw(self, surface, offset=(0, 0)):
        if self.age < 0:
            return
        super().draw(surface, offset)

class AngerParticle(Particle):
    def __init__(self, position):
        duration = random.random() * 0.5 + 0.5
        self.starting_radius = 5 + 3*random.random()
        vx = random.random() * 100 * random.choice((-1, 1))
        vy = random.random() * 125 * random.choice((-1,))
        x, y = position
        x += vx/abs(vx) * c.TILE_WIDTH//2
        y += vy/abs(vy) * c.TILE_HEIGHT//2
        super().__init__(position=(x, y), velocity=(vx, vy), duration=duration)
        self.age = -0.1

    def update(self, dt, events):
        self.radius = self.starting_radius * (1 - (self.through())**2)
        self.vx *= 0.1**dt
        self.vy *= 0.1**dt
        self.color = (200 - 64*self.through(),)*3
        super().update(dt, events)

    def draw(self, surface, offset=(0, 0)):
        if self.age < 0:
            return
        super().draw(surface, offset)