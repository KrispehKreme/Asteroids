"""Real assertions for GameState (score, lives, combo multiplier, high-score,
game-over state) -- test_harness_baseline.py deliberately covers only
CircleShape/constants, so this file closes that gap. Every test isolates
_load_high_score/_save_high_score from the real repo's highscore.json via
monkeypatch.chdir(tmp_path), since GameState() reads that file on construction.
"""
import json
from pathlib import Path

import pytest

from game_state import GameState


@pytest.fixture
def isolated(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    return GameState()


def test_add_score_uses_default_multiplier(isolated):
    isolated.add_score(100)
    assert isolated.score == 100


def test_add_score_applies_current_multiplier(isolated):
    isolated.multiplier = 2.0
    isolated.add_score(50)
    assert isolated.score == 100


def test_add_score_rounds(isolated):
    isolated.multiplier = 1.5
    isolated.add_score(11)
    assert isolated.score == round(11 * 1.5)


def test_lose_life_decrements_lives(isolated):
    isolated.lose_life()
    assert isolated.lives == 2
    assert isolated.game_over is False


def test_lose_life_resets_combo_and_multiplier(isolated):
    for _ in range(5):
        isolated.register_kill()
    assert isolated.multiplier == 1.5
    isolated.lose_life()
    assert isolated.combo_count == 0
    assert isolated.multiplier == 1.0


def test_lose_life_at_last_life_sets_game_over(isolated):
    isolated.lives = 1
    isolated.lose_life()
    assert isolated.lives == 0
    assert isolated.game_over is True


def test_lose_life_never_goes_below_zero(isolated):
    isolated.lives = 0
    isolated.lose_life()
    assert isolated.lives == 0
    assert isolated.game_over is True


def test_lose_life_at_zero_lives_saves_high_score(isolated):
    isolated.lives = 1
    isolated.score = 500
    isolated.lose_life()
    assert Path("highscore.json").exists()
    assert json.loads(Path("highscore.json").read_text()) == {"high_score": 500}


@pytest.mark.parametrize(
    "kill_count, expected_multiplier",
    [
        (4, 1.0),   # no bump yet
        (5, 1.5),   # 1st bump, at the 5th kill
        (9, 1.5),   # still 1 bump
        (10, 2.0),  # 2nd bump
        (19, 2.5),  # 3 bumps (5, 10, 15)
        (20, 3.0),  # 4 bumps (5, 10, 15, 20) -- reaches the cap exactly
        (25, 3.0),  # 5th bump would exceed the cap; min() holds it at 3.0
    ],
)
def test_register_kill_bumps_multiplier_every_5th_kill(isolated, kill_count, expected_multiplier):
    for _ in range(kill_count):
        isolated.register_kill()
    assert isolated.combo_count == kill_count
    assert isolated.multiplier == expected_multiplier


def test_reset_restores_starting_state(isolated):
    isolated.score = 1000
    isolated.lives = 1
    isolated.game_over = True
    isolated.combo_count = 5
    isolated.multiplier = 3.0

    isolated.reset()

    assert isolated.score == 0
    assert isolated.lives == 3
    assert isolated.game_over is False
    assert isolated.combo_count == 0
    assert isolated.multiplier == 1.0


def test_save_high_score_only_overwrites_when_beaten(isolated, tmp_path):
    isolated.score = 100
    isolated._save_high_score()
    assert json.loads(Path("highscore.json").read_text()) == {"high_score": 100}

    isolated.score = 50
    isolated._save_high_score()
    assert json.loads(Path("highscore.json").read_text()) == {"high_score": 100}


def test_load_high_score_reads_back_a_saved_value(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    Path("highscore.json").write_text(json.dumps({"high_score": 777}))
    state = GameState()
    assert state.high_score == 777


def test_load_high_score_defaults_to_zero_when_missing(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    state = GameState()
    assert state.high_score == 0
