import random
from math import fabs
from typing import Tuple

import pygame
from pygame.color import Color
from pygame.surface import Surface

from ball import Ball
from rectangle import Rectangle


def random_float(start, end):
    return (random.random() * (end - start)) + start

def random_sign():
    if random.getrandbits(1) == 0:
        return 1
    else:
        return -1

class PlayerPaddle:
    bounds: Rectangle
    y_speed: float

    def __init__(self, screen_size: Tuple[float, float]):
        self.bounds = Rectangle(width=25, height=75)
        self.bounds.x = screen_size[0] * 0.15 - self.bounds.width * 0.5
        self.bounds.y = screen_size[1] * 0.5 - self.bounds.height * 0.5
        self.y_speed = 500

    def update(self, screen_height, delta_time):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.bounds.y -= self.y_speed * delta_time
        if keys[pygame.K_DOWN]:
            self.bounds.y += self.y_speed * delta_time
        if self.bounds.y < 0:
            self.bounds.y = 0
        if self.bounds.y + self.bounds.height > screen_height:
            self.bounds.y = screen_height - self.bounds.height

    def display(self, surface: Surface, color: Color):
        self.bounds.display(surface, color)


class AIPaddle:
    bounds: Rectangle
    y_speed: float
    target_y: float

    def __init__(self, screen_size: Tuple[float, float]):
        self.bounds = Rectangle(width=25, height=75)
        self.bounds.x = screen_size[0] * 0.85 - self.bounds.width * 0.5
        self.bounds.y = screen_size[1] * 0.5 - self.bounds.height * 0.5
        self.target_y = self.bounds.y
        self.y_speed = 0

    def update(self, ball: Ball, screen_height, delta_time):
        if fabs(self.target_y - self.bounds.y) < 1:
            self.target_y = ball.bounds.y + (random_float(0, 10) * random_sign())
            while self.target_y + self.bounds.height > screen_height:
                self.target_y -= self.bounds.height
            if self.target_y < 0:
                self.target_y = 0
            time = random_float(.25, .65)
            # d = yf - yi
            # d = r * t
            # r = d / t
            # r = (yf - yi) / t
            delta_y = self.target_y - self.bounds.y
            self.y_speed = fabs(delta_y / time)

        if self.bounds.y > self.target_y:
            self.bounds.y -= self.y_speed * delta_time
        if self.bounds.y < self.target_y:
            self.bounds.y += self.y_speed * delta_time
        if self.bounds.y < 0:
            self.bounds.y = 0
        if self.bounds.y + self.bounds.height > screen_height:
            self.bounds.y = screen_height - self.bounds.height
        pass

    def display(self, surface: Surface, color: Color):
        self.bounds.display(surface, color)
