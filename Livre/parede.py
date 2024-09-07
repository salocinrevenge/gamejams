import pygame
import random

class Parede():
    def __init__(self, bioma, x, y) -> None:
        self.bioma = bioma
        self.x = x
        self.y = y
        
        self.imagem = self.getImage()
    
    def getImage(self):
        if self.bioma == "O":
            return pygame.image.load(f"assets/borda.png")
        return pygame.image.load(f"assets/borda.png")

    def clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)

    def render(self, screen, camera, deslocamento):
        # mostra a imagem
        camera.render(screen, self.imagem, (self.x+deslocamento[0], self.y+deslocamento[1]))

    def tick(self):
        pass
