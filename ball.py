import math
import random

from pygame.color import Color
from pygame.surface import Surface

from rectangle import Rectangle
from vector2 import Vector2


class Ball:
    bounds: Rectangle
    velocity: Vector2
    speed: float

    def __init__(self):
        self.bounds = Rectangle(width=25, height=25)
        self.velocity = Vector2()
        self.speed = 500

    def reset(self, width, height):
        self.bounds.x = (width * 0.5) - (self.bounds.width * 0.5)
        self.bounds.y = (height * 0.5) - (self.bounds.height * 0.5)
        radians = random.random() * (math.pi * 2)
        self.velocity.x = self.speed * math.cos(radians)
        self.velocity.y = self.speed * math.sin(radians)

    def update(self, screen_width, screen_height, delta_time):
        self.bounds.add_vector2_to_pos(self.velocity, delta_time)
        if self.bounds.y < 0:
            self.bounds.y = 0
            self.bounce_y()
        if self.bounds.y + self.bounds.height > screen_height:
            self.bounds.y = screen_height - self.bounds.height
            self.bounce_y()

    def bounce_x(self):
        self.velocity.x *= -1

    def bounce_y(self):
        self.velocity.y *= -1

    def collide_left(self, left_rect: Rectangle):
        if self.bounds.overlaps(left_rect):
            self.bounds.x = left_rect.x + left_rect.width
            self.bounce_x()

    def collide_right(self, right_rect: Rectangle):
        if self.bounds.overlaps(right_rect):
            self.bounds.x = right_rect.x - self.bounds.width
            self.bounce_x()

    def display(self, surface: Surface, color: Color):
        self.bounds.display(surface, color)
