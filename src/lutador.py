import pygame
from config import *


class Lutador:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 80, 180)
        self.vel = 0
        self.jump = False
        self.attack_type = 0

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), self.rect)

    def attack(self, surface):
        attacking_rect = pygame.Rect(self.rect.centerx, self.rect.y, 2 * self.rect.width, self.rect.height)
        pygame.draw.rect(surface, (0, 0, 255), attacking_rect)


    def move(self, num, surface):
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
            # attack
            if key[pygame.K_r] or key[pygame.K_f]:

                # tipo de ataque
                if key[pygame.K_r]:
                    self.attak_type = 1
                    self.attack(surface)
                if key[pygame.K_f]:
                    self.attak_type = 2

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