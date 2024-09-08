import pygame
import random
from personagem import Personagem

class Pinguim(Personagem):
    
    imagem = {"frente": pygame.image.load("assets/pinguim.png")}
    def __init__(self, mundo, sala, x, y) -> None:
        self.mundo = mundo
        self.x = x
        self.y = y
        self.sala = sala

    def render(self, screen, camera, deslocamento):
        camera.render(screen, self.imagem["frente"], (self.x+deslocamento[0], self.y+deslocamento[1]))

    def tick(self):
        pass
    
    def abrir(self):
        self.estado = "open"
        return self.conteudo
