import pygame
import random

class Chao():
    def __init__(self, bioma, x, y) -> None:
        self.bioma = bioma
        self.x = x
        self.y = y
        
        self.imagem = self.getImage()
    
    def getImage(self):
        if self.bioma == "O":
            return pygame.image.load(f"assets/water.png")
        if self.bioma == "D":
            return pygame.image.load(f"assets/desert.png")
        if self.bioma == "A":
            return pygame.image.load(f"assets/water.png")
        return pygame.image.load(f"assets/borda.png")

    def clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)

    def render(self, screen, camera, deslocamento):
        # mostra a imagem
        camera.render(screen, self.imagem, (self.x+deslocamento[0]+1, self.y+deslocamento[1]+1))

    def tick(self):
        pass
