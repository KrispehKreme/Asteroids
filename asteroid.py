"""Defines the Asteroid class, which splits into smaller asteroids when destroyed."""

from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, score_for_kind
import pygame
from logger import log_event
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def score_value(self):
        return score_for_kind(self.radius)

    def draw(self, screen):
        pygame.draw.circle(screen, color="white", center=self.position, radius=self.radius, width=LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt
        self.wrap_position()

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")
            random_angle = random.uniform(20,50)
            asteroid_one = self.velocity.rotate(random_angle)
            asteroid_two = self.velocity.rotate(-random_angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            Asteroid(self.position.x, self.position.y, new_radius).velocity = asteroid_one * 1.2
            Asteroid(self.position.x, self.position.y, new_radius).velocity = asteroid_two * 1.2
