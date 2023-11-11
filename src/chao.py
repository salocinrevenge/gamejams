import pygame

class Chao():
    def __init__(self, bioma, x, y, escala) -> None:
        self.bioma = bioma
        self.x = x
        self.y = y
        self.escala = escala
    
    cores = {"I": (230,230,255), "U": (30,0,40),"S": (180,150,0),"P": (100,235,100),"F": (0,50,0),"R": (150,150,150),"M": (150,0,0),"D": (255,255,0),"O": (0,0,100),"B": (255,255,0)}

    def render(self, screen):
        pygame.draw.rect(screen, self.cores[self.bioma], pygame.Rect(self.x*self.escala, self.y*self.escala, self.escala, self.escala))
