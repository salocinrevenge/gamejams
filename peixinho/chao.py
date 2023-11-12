import pygame
import random

class Chao():
    def __init__(self, bioma, x, y, escala) -> None:
        self.bioma = bioma
        self.x = x
        self.y = y
        self.escala = escala
        self.cor = self.cores[self.bioma]
        self.cor = (self.clamp(self.cor[0]+random.randint(-5,5),0,255), self.clamp(self.cor[1]+random.randint(-5,5),0,255), self.clamp(self.cor[2]+random.randint(-5,5),0,255))

    def clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)
    
    cores = {"I": (230,230,255), "U": (10,0,16),"S": (180,150,0),"P": (60,180,80),"F": (0,50,0),"R": (150,150,150),"M": (150,0,0),"D": (210,210,0),"O": (0,0,100),"B": (255,255,0)}

    def render(self, screen):
        pygame.draw.rect(screen, self.cor, pygame.Rect(self.x*self.escala, self.y*self.escala, self.escala, self.escala))

    def tick(self):
        pass
