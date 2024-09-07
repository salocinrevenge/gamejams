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
            return pygame.image.load(f"assets/parede.png")
        if self.bioma == "D":
            return pygame.image.load(f"assets/desert.png")
        if self.bioma == "A":
            return pygame.image.load(f"assets/ice.png")
        return pygame.image.load(f"assets/parede.png")

    def clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)

    def render(self, screen, camera, deslocamento):
        # mostra a imagem
        camera.render(screen, self.imagem, (self.x+deslocamento[0], self.y+deslocamento[1]))

    def tick(self):
        pass
