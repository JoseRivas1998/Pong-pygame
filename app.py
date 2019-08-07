from typing import Tuple

import pygame
from pygame.surface import Surface

from ball import Ball
from paddle import PlayerPaddle, AIPaddle

# CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class App:
    size: Tuple[float, float]
    running: bool
    window_title: str
    screen: Surface
    font: pygame.font.Font
    ball: Ball
    player: PlayerPaddle
    ai_paddle: AIPaddle
    left_score: int
    right_score: int
    clock: pygame.time.Clock
    last_time: float
    delta_time: float

    def __init__(self, width, height, title):
        self.size = (width, height)
        self.running = False
        self.window_title = title

    def begin(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.window_title)
        self.clock = pygame.time.Clock()
        self.setup_game()
        self.last_time = 0
        self.running = True
        self.game_loop()

    def setup_game(self):
        self.font = pygame.font.Font("resources/font/prstartk.ttf", 36)
        self.ball = Ball()
        self.ball.reset(self.size[0], self.size[1])
        self.player = PlayerPaddle(self.size)
        self.ai_paddle = AIPaddle(self.size)
        self.left_score = 0
        self.right_score = 0

    def poll_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        pass

    def update(self):
        self.ball.update(self.size[0], self.size[1], self.delta_time)
        self.player.update(self.size[1], self.delta_time)
        self.ai_paddle.update(self.ball, self.size[1], self.delta_time)
        self.ball.collide_left(self.player.bounds)
        self.ball.collide_right(self.ai_paddle.bounds)
        if self.ball.bounds.x < -100:
            self.ball.reset(self.size[0], self.size[1])
            self.right_score += 1
        if self.ball.bounds.x > self.size[0] + 100:
            self.ball.reset(self.size[0], self.size[1])
            self.left_score += 1

    def draw(self):
        self.screen.fill(BLACK)

        self.draw_center()

        self.draw_text(self.font, str(self.left_score), (self.size[0] * 0.25, self.size[1] * 0.15))
        self.draw_text(self.font, str(self.right_score), (self.size[0] * 0.75, self.size[1] * 0.15))

        self.ball.display(self.screen, WHITE)
        self.player.display(self.screen, WHITE)
        self.ai_paddle.display(self.screen, WHITE)

        pygame.display.flip()
        pass

    def draw_center(self):
        rect_width = 10
        rect_height = 5
        rect_x = (self.size[0] * 0.5) - (rect_width * 0.5)
        rect_y = rect_height * 0.5
        while rect_y + rect_height < self.size[1]:
            pygame.draw.rect(self.screen, WHITE, pygame.rect.Rect(rect_x, rect_y, rect_width, rect_height))
            rect_y += rect_height * 2

    def draw_text(self, font: pygame.font.Font, string, center: Tuple[float, float]):
        text = font.render(string, False, WHITE)
        text_rect = text.get_rect()
        text_rect.center = center
        self.screen.blit(text, text_rect)

    def step(self):
        self.poll_event()
        self.update()
        self.draw()

    def calculate_delta_time(self):
        current_time = pygame.time.get_ticks()
        self.delta_time = (current_time - self.last_time) / 1000.0
        self.last_time = current_time

    def game_loop(self):
        while self.running:
            self.calculate_delta_time()
            self.step()
            # self.clock.tick(60)
