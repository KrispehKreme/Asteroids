"""Real assertions for pure-ish game logic, used as ground truth by
scripts/eval-local-model.sh (in the claude-daemon workspace) to grade
model-generated changes to this repo. Asteroids has no test suite of its
own -- this file only covers logic that doesn't need a display surface
(pygame.Vector2/Sprite work headlessly; rendering does not).
"""
from circleshape import CircleShape
from constants import ASTEROID_KINDS, ASTEROID_MAX_RADIUS, ASTEROID_MIN_RADIUS, SCREEN_HEIGHT, SCREEN_WIDTH


def test_asteroid_max_radius_derived_from_kinds():
    assert ASTEROID_MAX_RADIUS == ASTEROID_MIN_RADIUS * ASTEROID_KINDS


def test_collides_with_true_when_overlapping():
    a = CircleShape(0, 0, 10)
    b = CircleShape(5, 0, 10)
    assert a.collides_with(b)


def test_collides_with_false_when_far_apart():
    a = CircleShape(0, 0, 10)
    b = CircleShape(1000, 1000, 10)
    assert not a.collides_with(b)


def test_collides_with_exact_touching_edge_counts_as_collision():
    a = CircleShape(0, 0, 10)
    b = CircleShape(20, 0, 10)
    assert a.collides_with(b)


def test_wrap_position_wraps_left_edge_to_right():
    shape = CircleShape(0, 0, 10)
    shape.position.x = -shape.radius - 1
    shape.wrap_position()
    assert shape.position.x == SCREEN_WIDTH + shape.radius


def test_wrap_position_wraps_right_edge_to_left():
    shape = CircleShape(0, 0, 10)
    shape.position.x = SCREEN_WIDTH + shape.radius + 1
    shape.wrap_position()
    assert shape.position.x == -shape.radius


def test_wrap_position_wraps_top_and_bottom():
    shape = CircleShape(0, 0, 10)
    shape.position.y = -shape.radius - 1
    shape.wrap_position()
    assert shape.position.y == SCREEN_HEIGHT + shape.radius

    shape.position.y = SCREEN_HEIGHT + shape.radius + 1
    shape.wrap_position()
    assert shape.position.y == -shape.radius


def test_wrap_position_noop_when_onscreen():
    shape = CircleShape(100, 100, 10)
    shape.wrap_position()
    assert shape.position.x == 100
    assert shape.position.y == 100
