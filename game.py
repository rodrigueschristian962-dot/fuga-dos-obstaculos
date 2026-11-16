
import random
import pygame

from settings import (
    LARGURA, ALTURA, FPS, TITULO,
    PRETO, BRANCO, AZUL, AMARELO, CINZA,
    VERMELHO, LARANJA
)
from player import Player
from meteors import Meteor
from coins import Coin
from particles import ParticleSystem
from ui import UI


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption(TITULO)

        self.clock = pygame.time.Clock()
        self.player = Player()
        self.ui = UI()
        self.particles = ParticleSystem()

        self.meteors = []
        self.coins = []

        self.state = "menu"
        self.score = 0
        self.record = self.load_record()
        self.time = 0

        self.stars = []
        for _ in range(90):
            self.stars.append([
                random.randint(0, LARGURA),
                random.randint(0, ALTURA),
                random.randint(1, 3),
                random.uniform(0.5, 2)
            ])

    def load_record(self):
        try:
            with open("recorde.txt", "r") as file:
                return int(file.read())
        except (FileNotFoundError, ValueError):
            return 0

    def save_record(self):
        with open("recorde.txt", "w") as file:
            file.write(str(self.record))

    def reset_game(self):
        self.player = Player()
        self.meteors.clear()
        self.coins.clear()
        self.particles = ParticleSystem()
        self.score = 0
        self.time = 0
        self.state = "playing"

    def draw_background(self):
        self.screen.fill((5, 10, 28))

        for star in self.stars:
            x, y, size, speed = star

            pygame.draw.circle(
                self.screen,
                (160, 210, 255),
                (int(x), int(y)),
                size
            )

            star[1] += speed

            if star[1] > ALTURA:
                star[1] = 0
                star[0] = random.randint(0, LARGURA)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                if event.key == pygame.K_RETURN:
                    if self.state in ("menu", "game_over"):
                        self.reset_game()

        return True

    def update_game(self):
        self.time += 1

        keys = pygame.key.get_pressed()
        self.player.update(keys)

        speed = 4 + self.score // 100

        if self.time % 48 == 0:
            self.meteors.append(Meteor())

        if self.time % 100 == 0:
            self.coins.append(Coin())

        for meteor in self.meteors[:]:
            meteor.update()
            meteor.draw(self.screen)

            if self.player.rect.colliderect(meteor.rect):
                self.particles.emit(
                    self.player.rect.centerx,
                    self.player.rect.centery,
                    LARANJA,
                    35
                )
                self.state = "game_over"
                break

            if meteor.is_off_screen():
                self.meteors.remove(meteor)

        if self.state == "game_over":
            return

        for coin in self.coins[:]:
            coin.update()
            coin.draw(self.screen)

            if self.player.rect.colliderect(coin.rect):
                self.score += coin.get_points()

                self.particles.emit(
                    coin.x, coin.y, AMARELO, 12
                )

                self.coins.remove(coin)

            elif coin.is_off_screen():
                self.coins.remove(coin)

        if self.time % 10 == 0:
            self.score += 1

        if self.score > self.record:
            self.record = self.score
            self.save_record()

        self.player.draw(self.screen)

        self.particles.update()
        self.particles.draw(self.screen)

        self.ui.draw_hud(
            self.screen,
            self.score,
            self.record
        )

    def run(self):
        running = True

        while running:
            self.clock.tick(FPS)
            running = self.handle_events()

            self.draw_background()

            if self.state == "menu":
                self.ui.draw_menu(self.screen)

            elif self.state == "playing":
                self.update_game()

            elif self.state == "game_over":
                self.particles.update()
                self.particles.draw(self.screen)

                self.ui.draw_game_over(
                    self.screen,
                    self.score,
                    self.record
                )

            pygame.display.flip()

        pygame.quit()
