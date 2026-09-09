"""Generates and manages the game's sound effects."""

import array
import math
import random
import pygame

SAMPLE_RATE = 44100
MASTER_VOLUME = 0.7


def sine_wave(frequency, duration, sample_rate=SAMPLE_RATE):
    length = int(duration * sample_rate)
    wave = array.array('h')
    for i in range(length):
        t = i / sample_rate
        value = int(32767 * MASTER_VOLUME * math.sin(2 * math.pi * frequency * t))
        wave.append(value)
    return wave


def noise_wave(duration, sample_rate=SAMPLE_RATE):
    length = int(duration * sample_rate)
    wave = array.array('h')
    for _ in range(length):
        value = int(32767 * MASTER_VOLUME * (random.random() * 2 - 1))
        wave.append(value)
    return wave


def fade_out(wave, fade_duration=0.01):
    length = len(wave)
    fade_length = min(int(fade_duration * SAMPLE_RATE), length - 1)
    for i in range(fade_length):
        fade_factor = (fade_length - i) / fade_length
        wave[length - 1 - i] = int(wave[length - 1 - i] * fade_factor)


class SoundManager:
    def __init__(self):
        self.enabled = False
        self.shoot = None
        self.explosion = None
        self.thrust = None

        try:
            # Explicit format (not pre_init) since pygame.init() may have
            # already brought the mixer up with different defaults by the
            # time this runs; init() can be called again to force a format.
            pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1)
        except Exception:
            return

        try:
            shoot_wave = sine_wave(1000, 0.08)
            fade_out(shoot_wave, 0.01)
            self.shoot = pygame.mixer.Sound(buffer=shoot_wave.tobytes())

            explosion_wave = noise_wave(0.3)
            fade_out(explosion_wave, 0.2)
            self.explosion = pygame.mixer.Sound(buffer=explosion_wave.tobytes())

            thrust_wave = sine_wave(100, 0.15)
            fade_out(thrust_wave, 0.05)
            self.thrust = pygame.mixer.Sound(buffer=thrust_wave.tobytes())

            self.enabled = True
        except Exception:
            self.enabled = False

    def play_shoot(self):
        if not self.enabled or not self.shoot:
            return
        try:
            self.shoot.play()
        except pygame.error:
            pass

    def play_explosion(self):
        if not self.enabled or not self.explosion:
            return
        try:
            self.explosion.play()
        except pygame.error:
            pass

    def play_thrust(self):
        if not self.enabled or not self.thrust:
            return
        try:
            self.thrust.play()
        except pygame.error:
            pass
