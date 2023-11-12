import random
from melancia import Melancia
import pygame

class Melanceira():
    def __init__(self, x, y, sala, tempoColheita = 30): # 30 random tick speed
        self.x = x
        self.y = y
        self.sala = sala
        self.tempoColheita = tempoColheita + random.randint(0, tempoColheita//2)
        self.tempo = random.randint(0, tempoColheita//2)
        self.escala = sala.escala
        self.fruta = None

    def tick(self):
        self.tempoColheita+=1
        if self.tempo > self.tempoColheita:
            self.fruta = Melancia(self.x, self.y, self.sala)

    def render(self, screen):
        #print desenha a arvore de melancia


        # desenha flor
        if self.tempo > self.tempoColheita//2:
            pygame.draw.circle(screen, (255, 0, 0), (self.x*self.escala+self.escala//2, self.y*self.escala+self.escala//2), self.escala//2)
        if self.fruta != None:
            self.fruta.render(screen)
        
