import pygame
import random
from semente import Semente
class Melancia():
    def __init__(self, x, y, sala) -> None:
        self.x = x
        self.y = y
        self.sala = sala
        self.escala = sala.escala
        self.semente = None
        if random.randint(0, 100) < 30: # 30 % de chance de conter semente
            self.semente = Semente()
        self.energia = random.randint(500, 1000)

    def render(self, screen):
        # desenha elipse
        pygame.draw.ellipse(screen, (0, 110, 0), pygame.Rect(self.x*self.escala+19, self.y*self.escala+20, 16*self.escala//40, 20*self.escala//40))

    def renderItem(self, screen,x,y,escala):
        pygame.draw.ellipse(screen, (0, 110, 0), pygame.Rect(x+2, y+2, 16*escala, 20*escala))
    
    def comer(self):
        return self.energia, self.semente