import pygame
import random
from personagem import Personagem

class Pinguim(Personagem):
    
    imagem = {"frente": pygame.image.load("assets/pinguim.png")}
    def __init__(self, mundo, sala, x, y) -> None:
        super().__init__(x, y, mundo)
        self.mundo = mundo
        self.x = x
        self.y = y
        self.sala = sala
        self.intervaloPassosMax = 10
        self.demanda = (0, 0)


    def render(self, screen, camera, deslocamento):
        camera.render(screen, self.imagem["frente"], (self.x+deslocamento[0], self.y+deslocamento[1]))
        super().render(screen, camera, deslocamento)
        
    acoes = ["a", "d", "w", "s"]
    pos = {"a": (-1, 0), "d": (1, 0), "w": (0, -1), "s": (0, 1)}
        
    def think(self):
        self.demanda = self.pos[random.choice(self.acoes)]

    def tick(self):
        self.intervaloPassos -= 1
        if self.intervaloPassos <= 0:
            self.sala.mover(self, self.x, self.y, self.x+self.demanda[0], self.y+self.demanda[1])
            # self.sala.moverEntidade(self, self.x, self.y, self.x+self.demanda[0], self.y+self.demanda[1])
            self.intervaloPassos = self.intervaloPassosMax
        super().tick()
