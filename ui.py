
import pygame

from settings import (
    LARGURA,
    ALTURA,
    BRANCO,
    AZUL,
    AMARELO,
    VERMELHO,
    CINZA,
    PRETO,
)


class UI:
    def __init__(self):
        self.title_font = pygame.font.Font(None, 58)
        self.medium_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 25)

    def draw_text(self, screen, text, font, color, x, y):
        surface = font.render(str(text), True, color)
        rect = surface.get_rect(center=(x, y))
        screen.blit(surface, rect)

    def draw_menu(self, screen):
        screen.fill(PRETO)

        self.draw_text(
            screen, "FUGA DOS", self.title_font,
            AZUL, LARGURA // 2, 190
        )

        self.draw_text(
            screen, "OBSTACULOS", self.title_font,
            AMARELO, LARGURA // 2, 245
        )

        self.draw_text(
            screen, "Desvie dos meteoros!", self.medium_font,
            BRANCO, LARGURA // 2, 330
        )

        self.draw_text(
            screen, "Pressione ENTER para jogar",
            self.medium_font, BRANCO,
            LARGURA // 2, 420
        )

        self.draw_text(
            screen, "Use as setas ou WASD",
            self.small_font, CINZA,
            LARGURA // 2, 465
        )

    def draw_hud(self, screen, score, record):
        score_text = self.small_font.render(
            f"Pontos: {score}", True, BRANCO
        )

        record_text = self.small_font.render(
            f"Recorde: {record}", True, AMARELO
        )

        screen.blit(score_text, (15, 15))
        screen.blit(record_text, (15, 45))

    def draw_game_over(self, screen, score, record):
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(190)
        overlay.fill(PRETO)
        screen.blit(overlay, (0, 0))

        self.draw_text(
            screen, "GAME OVER", self.title_font,
            VERMELHO, LARGURA // 2, 220
        )

        self.draw_text(
            screen, f"Pontuacao: {score}", self.medium_font,
            BRANCO, LARGURA // 2, 300
        )

        self.draw_text(
            screen, f"Recorde: {record}", self.medium_font,
            AMARELO, LARGURA // 2, 345
        )

        self.draw_text(
            screen, "ENTER para jogar novamente",
            self.small_font, BRANCO,
            LARGURA // 2, 430
        )

        self.draw_text(
            screen, "ESC para sair",
            self.small_font, CINZA,
            LARGURA // 2, 470
        )
