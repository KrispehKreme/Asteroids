STARTING_LIVES = 3


class GameState:
    """Tracks score, lives, and game-over/restart status for a single session."""

    def __init__(self):
        self.score = 0
        self.lives = STARTING_LIVES
        self.game_over = False

    def add_score(self, points):
        self.score += points

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True

    def reset(self):
        self.score = 0
        self.lives = STARTING_LIVES
        self.game_over = False
