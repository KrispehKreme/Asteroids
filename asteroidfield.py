import pygame
import random
from asteroid import Asteroid
from constants import *

class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.elapsed = 0.0

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def difficulty(self):
        """0.0 at round start, ramping to 1.0 by DIFFICULTY_RAMP_SECONDS."""
        return min(self.elapsed / DIFFICULTY_RAMP_SECONDS, 1.0)

    def current_spawn_rate(self):
        t = self.difficulty()
        return ASTEROID_SPAWN_RATE_SECONDS + t * (
            ASTEROID_SPAWN_RATE_MIN_SECONDS - ASTEROID_SPAWN_RATE_SECONDS
        )

    def current_speed_range(self):
        t = self.difficulty()
        start_low, start_high = ASTEROID_SPEED_RANGE_START
        end_low, end_high = ASTEROID_SPEED_RANGE_END
        low = start_low + t * (end_low - start_low)
        high = start_high + t * (end_high - start_high)
        return low, high

    def update(self, dt):
        self.elapsed += dt
        self.spawn_timer += dt
        if self.spawn_timer > self.current_spawn_rate():
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed_low, speed_high = self.current_speed_range()
            speed = random.randint(round(speed_low), round(speed_high))
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)