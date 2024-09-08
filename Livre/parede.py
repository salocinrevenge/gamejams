import pygame
import random

class Parede():
    def __init__(self, bioma, x, y) -> None:
        self.bioma = bioma
        self.x = x
        self.y = y
        
        self.imagem = self.getImage()
        
    imagens = {
                "o": pygame.image.load("assets/rock.png"), "d": pygame.image.load("assets/wall desert.png"),
                "a": pygame.image.load("assets/wall ice.png"), "j": pygame.image.load("assets/tree.png"),
                "default": pygame.image.load("assets/parede.png"), "apple": pygame.image.load("assets/tree with apple.png")
              }
    
    def getImage(self):
        self.bioma = self.bioma.lower()
        self.b = self.bioma
        if self.b not in self.imagens.keys():
            self.b = "default"
        if self.b == "j":
            if random.random() < 0.4:
                self.b = "apple"
            

    def clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)

    def render(self, screen, camera, deslocamento):
        camera.render(screen, self.imagens[self.b], (self.x+deslocamento[0], self.y+deslocamento[1]))

    def tick(self):
        pass
