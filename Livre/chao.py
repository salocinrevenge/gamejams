import pygame
import random

class Chao():
    def __init__(self, bioma, x, y) -> None:
        self.bioma = bioma
        self.x = x
        self.y = y
        self.imagem = pygame.image.load(f"assets/tile.png")

    def clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)

    def render(self, screen):
        # mostra a imagem
        screen.blit(self.imagem, (self.x, self.y))
        print(self.x, self.y)

    def tick(self):
        pass
