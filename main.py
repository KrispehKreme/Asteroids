import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player
from logger import log_state, log_event
from asteroidfield import AsteroidField
from asteroid import Asteroid
from shot import Shot
from game_state import GameState
from hud import Hud


def start_new_round(groups):
    updatable, drawable, asteroids, shots = groups
    updatable.empty()
    drawable.empty()
    asteroids.empty()
    shots.empty()

    asteroid_field = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
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
    player, asteroid_field = start_new_round(groups)

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
                player, asteroid_field = start_new_round(groups)
            elif keys[pygame.K_ESCAPE]:
                pygame.quit()
                return
        else:
            updatable.update(dt)

            for asteroid in list(asteroids):
                if not player.is_invulnerable() and player.collides_with(asteroid):
                    log_event("player_hit")
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
                        asteroid.split()
                        shot.kill()

        screen.fill("black")

        for sprite in drawable:
            sprite.draw(screen)

        hud.draw(screen, game_state)

        pygame.display.flip()


if __name__ == "__main__":
    main()
