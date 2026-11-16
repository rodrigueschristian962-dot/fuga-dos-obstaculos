
import math
import random
import pygame

from settings import (
    LARGURA,
    ALTURA,
    METEORO_MIN_TAMANHO,
    METEORO_MAX_TAMANHO,
    METEORO_VELOCIDADE_MIN,
    METEORO_VELOCIDADE_MAX,
    LARANJA,
    VERMELHO,
    CINZA,
)


class Meteor:
    def __init__(self):
        self.radius = random.randint(
            METEORO_MIN_TAMANHO,
            METEORO_MAX_TAMANHO
        )

        self.x = random.randint(
            self.radius,
            LARGURA - self.radius
        )

        self.y = -self.radius * 2

        self.speed = random.uniform(
            METEORO_VELOCIDADE_MIN,
            METEORO_VELOCIDADE_MAX
        )

        self.angle = 0
        self.rotation_speed = random.uniform(-2, 2)

        self.points = []

        for i in range(10):
            angle = (2 * math.pi * i) / 10
            distance = self.radius * random.uniform(0.75, 1.15)

            px = math.cos(angle) * distance
            py = math.sin(angle) * distance

            self.points.append((px, py))

        self.rect = pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def update(self, extra_speed=0):
        self.y += self.speed + extra_speed
        self.angle += self.rotation_speed

        self.rect.center = (int(self.x), int(self.y))

    def draw(self, screen):
        rotated_points = []

        for px, py in self.points:
            angle = math.radians(self.angle)

            rotated_x = (
                px * math.cos(angle)
                - py * math.sin(angle)
            )

            rotated_y = (
                px * math.sin(angle)
                + py * math.cos(angle)
            )

            rotated_points.append((
                int(self.x + rotated_x),
                int(self.y + rotated_y)
            ))

        pygame.draw.polygon(
            screen,
            CINZA,
            rotated_points
        )

        pygame.draw.polygon(
            screen,
            LARANJA,
            rotated_points,
            3
        )

        pygame.draw.circle(
            screen,
            VERMELHO,
            (
                int(self.x - self.radius * 0.25),
                int(self.y - self.radius * 0.15)
            ),
            max(3, self.radius // 5)
        )

    def is_off_screen(self):
        return self.y - self.radius > ALTURA
