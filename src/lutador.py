import pygame
from config import *


class Lutador:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 80, 180)
        self.vel = 0
        self.jump = False

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), self.rect)

    def move(self, num):
        dx = 0
        dy = 0

        # Pegando as teclas
        key = pygame.key.get_pressed()
        if(num):
            if(key[pygame.K_a]):
                dx = -SPEED
            if (key[pygame.K_d]):
                dx = SPEED
            # jump
            if key[pygame.K_w] and not self.jump:
                self.vel = -30
                self.jump = True

        # Aplicando gravidade
        self.vel += GRAVITY
        dy += self.vel

        # Pra n sair da tela
        if self.rect.left + dx < 0:
            dx = 0 - self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right
        if self.rect.bottom + dy > SCREEN_HEIGHT - 80:
            self.vel = 0
            self.jump = False
            dy = SCREEN_HEIGHT - 80 - self.rect.bottom

        self.rect.x += dx
        self.rect.y += dy