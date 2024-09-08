import pygame
import random

class Bau():
    
    imagem = {"closed": pygame.image.load("assets/chest.png"), "open": pygame.image.load("assets/open chest.png")}
    def __init__(self, bioma, x, y) -> None:
        self.bioma = bioma
        self.x = x
        self.y = y
        self.estado = "closed"
        self.conteudo = []

    def render(self, screen, camera, deslocamento):
        camera.render(screen, self.imagem[self.estado], (self.x+deslocamento[0], self.y+deslocamento[1]))

    def tick(self):
        pass
    
    def abrir(self):
        self.estado = "open"
        return self.conteudo
