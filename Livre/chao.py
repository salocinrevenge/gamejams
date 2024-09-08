import pygame
import random

class Chao():
    
    imagens = {
                "o": pygame.image.load("assets/water.png"), "d": pygame.image.load("assets/desert.png"),
                "a": pygame.image.load("assets/ice.png"), "j": pygame.image.load("assets/grass.png"),
                "default": pygame.image.load("assets/borda.png")
              }
    def __init__(self, bioma, x, y) -> None:
        self.bioma = bioma
        self.x = x
        self.y = y
        self.b = self.bioma.lower()
        if self.b not in self.imagens.keys():
            self.b = "default"
        

    def clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)

    def render(self, screen, camera, deslocamento):
        camera.render(screen, self.imagens[self.b], (self.x+deslocamento[0]+1, self.y+deslocamento[1]+1))

    def tick(self):
        pass
