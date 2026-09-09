"""Particle effect objects used for visual effects like explosions."""

import pygame
import random


class Particle:
    def __init__(self, position, velocity, lifetime, color=(255, 255, 255), radius=2):
        self.position = position.copy()
        self.velocity = velocity.copy()
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.color = color
        self.radius = radius

    def update(self, dt):
        self.position += self.velocity * dt
        self.lifetime -= dt

    def is_dead(self):
        return self.lifetime <= 0

    def draw(self, screen):
        if self.is_dead():
            return
        fraction = self.lifetime / self.max_lifetime
        r = int(self.color[0] * fraction)
        g = int(self.color[1] * fraction)
        b = int(self.color[2] * fraction)
        pygame.draw.circle(screen, (r, g, b), (int(self.position.x), int(self.position.y)), self.radius)


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def spawn_burst(self, position, count=20, speed_range=(50, 200), lifetime_range=(0.3, 0.8), color=(255, 255, 255)):
        for _ in range(count):
            speed = random.uniform(*speed_range)
            angle = random.uniform(0, 360)
            velocity = pygame.Vector2(1, 0).rotate(angle) * speed
            lifetime = random.uniform(*lifetime_range)
            self.particles.append(Particle(position, velocity, lifetime, color))

    def update(self, dt):
        for p in self.particles[:]:
            p.update(dt)
            if p.is_dead():
                self.particles.remove(p)

    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)


class ScreenShake:
    def __init__(self):
        self.magnitude = 0
        self.duration = 0
        self.max_duration = 0

    def trigger(self, magnitude=8, duration=0.2):
        self.magnitude = magnitude
        self.duration = duration
        self.max_duration = duration

    def update(self, dt):
        if self.duration > 0:
            self.duration = max(0, self.duration - dt)

    def get_offset(self):
        if self.duration <= 0 or self.max_duration <= 0:
            return (0, 0)
        # Ease out: offset shrinks toward 0 as the shake's remaining
        # fraction (not raw seconds) approaches 0.
        fraction = self.duration / self.max_duration
        current_magnitude = self.magnitude * fraction
        offset_x = random.uniform(-current_magnitude, current_magnitude)
        offset_y = random.uniform(-current_magnitude, current_magnitude)
        return (int(offset_x), int(offset_y))
