import json

STARTING_LIVES = 3
HIGH_SCORE_FILE = "highscore.json"


def lives_remaining_after_loss(lives: int) -> int:
    return max(lives - 1, 0)


class GameState:
    """Tracks score, lives, and game-over/restart status for a single session."""

    def __init__(self):
        self.score = 0
        self.lives = STARTING_LIVES
        self.game_over = False
        self.high_score = self._load_high_score()
        self.combo_count = 0
        self.multiplier = 1.0

    def add_score(self, points):
        self.score += round(points * self.multiplier)

    def lose_life(self):
        self.lives = lives_remaining_after_loss(self.lives)
        if self.lives <= 0:
            self.game_over = True
            self._save_high_score()
        self.combo_count = 0
        self.multiplier = 1.0

    def register_kill(self):
        self.combo_count += 1
        if self.combo_count % 5 == 0:
            self.multiplier = min(self.multiplier + 0.5, 3.0)

    def reset(self):
        self.score = 0
        self.lives = STARTING_LIVES
        self.game_over = False
        self.combo_count = 0
        self.multiplier = 1.0

    def _load_high_score(self):
        try:
            with open(HIGH_SCORE_FILE) as f:
                return json.load(f).get("high_score", 0)
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            return 0

    def _save_high_score(self):
        if self.score <= self.high_score:
            return
        self.high_score = self.score
        try:
            with open(HIGH_SCORE_FILE, "w") as f:
                json.dump({"high_score": self.high_score}, f)
        except OSError:
            pass
