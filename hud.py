import pygame


class Hud:
    """Renders score, lives, and the game-over overlay."""

    def __init__(self):
        self.font = pygame.font.SysFont("arial", 28)
        self.big_font = pygame.font.SysFont("arial", 64)

    def draw(self, screen, game_state, high_score=None):
        score_surface = self.font.render(f"Score: {game_state.score}", True, "white")
        screen.blit(score_surface, (10, 10))

        lives_surface = self.font.render(f"Lives: {game_state.lives}", True, "white")
        screen.blit(lives_surface, (10, 40))

        if high_score is not None:
            high_score_surface = self.font.render(
                f"High Score: {high_score}", True, "white"
            )
            rect = high_score_surface.get_rect()
            rect.topright = (screen.get_width() - 10, 10)
            screen.blit(high_score_surface, rect)

        if game_state.game_over:
            self._draw_game_over(screen)

    def _draw_game_over(self, screen):
        game_over_surface = self.big_font.render("GAME OVER", True, "white")
        game_over_rect = game_over_surface.get_rect(
            center=(screen.get_width() / 2, screen.get_height() / 2 - 20)
        )
        screen.blit(game_over_surface, game_over_rect)

        prompt_surface = self.font.render(
            "Press R to restart or ESC to quit", True, "white"
        )
        prompt_rect = prompt_surface.get_rect(
            center=(screen.get_width() / 2, screen.get_height() / 2 + 40)
        )
        screen.blit(prompt_surface, prompt_rect)
