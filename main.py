import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player
from logger import log_state, log_event
from asteroidfield import AsteroidField
from asteroid import Asteroid
from shot import Shot
from game_state import GameState
from hud import Hud
from particles import ParticleSystem, ScreenShake
from sounds import SoundManager


def start_new_round(groups, sound_manager):
    updatable, drawable, asteroids, shots = groups
    updatable.empty()
    drawable.empty()
    asteroids.empty()
    shots.empty()

    asteroid_field = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, sound_manager=sound_manager)
    return player, asteroid_field


def main():
    print("Starting Asteroids with pygame version: ", pygame.version.ver)
    print("Screen width:", SCREEN_WIDTH)
    print("Screen height:", SCREEN_HEIGHT)

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    shots = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable, )
    Shot.containers = (updatable, drawable, shots)

    groups = (updatable, drawable, asteroids, shots)
    game_state = GameState()
    hud = Hud()
    particles = ParticleSystem()
    screen_shake = ScreenShake()
    sound_manager = SoundManager()
    frame_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    player, asteroid_field = start_new_round(groups, sound_manager)

    while True:
        dt = clock.tick(60) / 1000
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if game_state.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                game_state.reset()
                particles.particles.clear()
                player, asteroid_field = start_new_round(groups, sound_manager)
            elif keys[pygame.K_ESCAPE]:
                pygame.quit()
                return
        else:
            updatable.update(dt)
            particles.update(dt)
            screen_shake.update(dt)

            for asteroid in list(asteroids):
                if not player.is_invulnerable() and player.collides_with(asteroid):
                    log_event("player_hit")
                    particles.spawn_burst(player.position, count=30, color=(255, 80, 80))
                    screen_shake.trigger(magnitude=12, duration=0.35)
                    sound_manager.play_explosion()
                    game_state.lose_life()
                    if game_state.game_over:
                        print("Game over! Final score:", game_state.score)
                    else:
                        player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                        player.rotation = 0
                        player.make_invulnerable()

                for shot in list(shots):
                    if shot.collides_with(asteroid):
                        log_event("asteroid_shot")
                        game_state.add_score(asteroid.score_value())
                        game_state.register_kill()
                        particles.spawn_burst(asteroid.position, count=16)
                        screen_shake.trigger(magnitude=4, duration=0.15)
                        sound_manager.play_explosion()
                        asteroid.split()
                        shot.kill()

        frame_surface.fill("black")

        for sprite in drawable:
            sprite.draw(frame_surface)

        particles.draw(frame_surface)
        hud.draw(frame_surface, game_state)

        screen.fill("black")
        screen.blit(frame_surface, screen_shake.get_offset())

        pygame.display.flip()


if __name__ == "__main__":
    main()
