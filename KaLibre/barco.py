import pygame
import random

class Barco():
    
    imagem = pygame.image.load("assets/barco.png")
    def __init__(self, bioma, x, y) -> None:
        self.bioma = bioma
        self.x = x
        self.y = y

    def clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)

    def render(self, screen, camera, deslocamento):
        camera.render(screen, self.imagem, (self.x+deslocamento[0], self.y+deslocamento[1]))

    def setNavegante(self, navegante):
        self.navegante = navegante
        navegante.setBarco(self)

    def tick(self):
        pass
    
    def input(self, evento):
        pass
    
    def setPos(self, x, y):
        self.x = x
        self.y = y
