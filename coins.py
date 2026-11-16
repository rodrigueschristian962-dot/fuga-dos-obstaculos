
import math
import random
import pygame

from settings import (
    LARGURA,
    ALTURA,
    AMARELO,
    BRANCO,
    PONTOS_MOEDA,
)


class Coin:
    def __init__(self):
        self.radius = 12

        self.x = random.randint(
            self.radius,
            LARGURA - self.radius
        )

        self.y = -self.radius

        self.speed = random.uniform(2, 4)
        self.animation = random.uniform(0, math.pi * 2)

        self.rect = pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def update(self):
        self.y += self.speed
        self.animation += 0.12

        self.rect.center = (int(self.x), int(self.y))

    def draw(self, screen):
        pulse = abs(math.sin(self.animation))
        current_radius = int(self.radius * (0.8 + pulse * 0.2))

        pygame.draw.circle(
            screen,
            AMARELO,
            (int(self.x), int(self.y)),
            current_radius
        )

        pygame.draw.circle(
            screen,
            BRANCO,
            (int(self.x), int(self.y)),
            current_radius,
            2
        )

    def is_off_screen(self):
        return self.y - self.radius > ALTURA

    def get_points(self):
        return PONTOS_MOEDA
