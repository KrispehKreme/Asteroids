from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_SHOT_COOLDOWN_SECONDS, PLAYER_SPEED, PLAYER_TURN_SPEED, PLAYER_SHOOT_SPEED, PLAYER_INVULNERABILITY_SECONDS
from circleshape import CircleShape
import pygame
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown = 0
        self.invulnerable_timer = 0
    # in the Player class

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def is_invulnerable(self):
        return self.invulnerable_timer > 0

    def make_invulnerable(self, seconds=PLAYER_INVULNERABILITY_SECONDS):
        self.invulnerable_timer = seconds

    def draw(self, screen):
        # Blink while invulnerable so the player gets visible feedback
        # that they can't be hit yet, instead of it being invisible state.
        if self.is_invulnerable() and int(self.invulnerable_timer * 10) % 2 == 0:
            return
        pygame.draw.polygon(screen, color="white", points=self.triangle(), width=LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        self.shot_cooldown -= dt
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)

        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_w]:
            self.move(dt)
        
        if keys[pygame.K_s]:
            self.move(-dt)

        if keys[pygame.K_SPACE]:
            self.shoot()

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector
        self.wrap_position()

    def shoot(self):
        if self.shot_cooldown > 0:
            return
        else:
            Shot(self.position.x, self.position.y).velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
            self.shot_cooldown = PLAYER_SHOT_COOLDOWN_SECONDS
