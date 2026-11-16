
import pygame
from settings import (
    LARGURA,
    ALTURA,
    JOGADOR_LARGURA,
    JOGADOR_ALTURA,
    JOGADOR_VELOCIDADE,
    AZUL,
    BRANCO,
    LARANJA,
)


class Player:
    def __init__(self):
        self.x = LARGURA // 2 - JOGADOR_LARGURA // 2
        self.y = ALTURA - 110
        self.rect = pygame.Rect(
            self.x,
            self.y,
            JOGADOR_LARGURA,
            JOGADOR_ALTURA,
        )

    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= JOGADOR_VELOCIDADE

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += JOGADOR_VELOCIDADE

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= JOGADOR_VELOCIDADE

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += JOGADOR_VELOCIDADE

        self.x = max(0, min(self.x, LARGURA - JOGADOR_LARGURA))
        self.y = max(0, min(self.y, ALTURA - JOGADOR_ALTURA))

        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        # Chama da nave
        pygame.draw.polygon(
            screen,
            LARANJA,
            [
                (self.x + 10, self.y + JOGADOR_ALTURA - 5),
                (self.x + JOGADOR_LARGURA // 2, self.y + JOGADOR_ALTURA + 8),
                (self.x + JOGADOR_LARGURA - 10, self.y + JOGADOR_ALTURA - 5),
            ],
        )

        # Corpo da nave
        pygame.draw.polygon(
            screen,
            AZUL,
            [
                (self.x + JOGADOR_LARGURA // 2, self.y),
                (self.x + JOGADOR_LARGURA, self.y + JOGADOR_ALTURA - 8),
                (self.x + JOGADOR_LARGURA // 2, self.y + JOGADOR_ALTURA - 16),
                (self.x, self.y + JOGADOR_ALTURA - 8),
            ],
        )

        # Janela da nave
        pygame.draw.circle(
            screen,
            BRANCO,
            (self.x + JOGADOR_LARGURA // 2, self.y + 20),
            6,
        )
