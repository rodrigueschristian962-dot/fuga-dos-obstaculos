
import random
import pygame


class Particle:
    def __init__(self, x, y, color):
        self.x = float(x)
        self.y = float(y)
        self.color = color

        self.radius = random.randint(2, 5)
        self.life = random.randint(20, 40)
        self.max_life = self.life

        self.speed_x = random.uniform(-3, 3)
        self.speed_y = random.uniform(-3, 3)

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

        self.life -= 1
        self.radius = max(1, self.radius - 0.05)

    def draw(self, screen):
        if self.life > 0:
            pygame.draw.circle(
                screen,
                self.color,
                (int(self.x), int(self.y)),
                int(self.radius)
            )

    def is_alive(self):
        return self.life > 0


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, color, amount=15):
        for _ in range(amount):
            self.particles.append(
                Particle(x, y, color)
            )

    def update(self):
        for particle in self.particles:
            particle.update()

        self.particles = [
            particle
            for particle in self.particles
            if particle.is_alive()
        ]

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)
