import pygame
from config import *
from lutador import Lutador

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Game")
        self.running = True
        self.bg = pygame.image.load("assets/image/florest.jpg").convert_alpha()




    def play(self):

        lutador_1 = Lutador(200, 360)
        lutador_2 = Lutador(700, 360)


        while self.running:
            self._draw_background()
            lutador_1.draw(self.screen)
            lutador_2.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False


            pygame.display.update()
        pygame.quit()


    def _draw_background(self):
        scale_bg = pygame.transform.scale(self.bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(scale_bg, (0, 0))