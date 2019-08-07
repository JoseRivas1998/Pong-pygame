from pygame.color import Color
from pygame.draw import rect
from pygame.rect import Rect
from pygame.surface import Surface

from vector2 import Vector2


class Rectangle:
    x: float
    y: float
    width: float
    height: float

    def __init__(self, x=0, y=0, width=0, height=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def add_vector2_to_pos(self, v2: Vector2, scalar: float = 1):
        self.x += v2.x * scalar
        self.y += v2.y * scalar

    def overlaps(self, r):
        """

        :type r: Rectangle
        """
        b1 = self.x < r.x + r.width
        b2 = self.x + self.width > r.x
        b3 = self.y < r.y + r.height
        b4 = self.y + self.height > r.y
        return b1 and b2 and b3 and b4

    def display(self, surface: Surface, color: Color):
        rect(surface, color, Rect(self.x, self.y, self.width, self.height))
