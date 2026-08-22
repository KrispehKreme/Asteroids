# Asteroids

A small Asteroids clone built with pygame.

## Running

```
uv sync
uv run python main.py
```

## Controls

- `W` / `S` — thrust forward / backward
- `A` / `D` — rotate left / right
- `Space` — shoot
- `H` — hyperspace (panic-teleport to a random point on screen, 3s cooldown, no invulnerability on landing)
- `R` — restart after game over
- `Esc` — quit from the game-over screen

## Gameplay

- 3 lives; losing the last one ends the run and shows a restart prompt.
- Smaller asteroids are worth more points than larger ones.
- Spawn rate and asteroid speed ramp up gradually the longer you survive.
- High score persists between runs in `highscore.json` (gitignored, created on first play).
