import random
from melancia import Melancia
import pygame

class Melanceira():
    def __init__(self, x, y, sala, tempoColheita = 4): # 30 random tick speed
        self.x = x
        self.y = y
        self.sala = sala
        self.tempoColheita = tempoColheita + random.randint(0, tempoColheita//2)
        self.tempo = random.randint(0, tempoColheita//2)
        self.escala = sala.escala
        self.fruta = None
        self.fixedPontos = ((13,40),(17,36), (18,31), (17,26), (14,24), (11,22), (10,23), (11,24), (10,25), (9,25), (7,26), (3,26), (5,24), (7,22), (10,23), (11,21), (7,18), (6,13), (7,7), (11,4), (17,3), (23,5), (24,7), (26,4), (27,2), (28,2), (32,3), (34,4), (30,6), (24,9), (26,15), (28,20), (29,22), (26,22), (26,20), (25,18), (24,10), (19,5), (13,5), (9,8), (7,12), (9,10), (13,10), (14,13), (16,14), (14,15), (11,13), (9,12), (7,13), (8,16), (11,19), (15,22), (19,28), (20,32), (18,38), (18,40))
        self.pontos = []
        for ponto in self.fixedPontos:
            self.pontos.append((ponto[0]+self.x*self.escala, ponto[1]+self.y*self.escala))

    def tick(self):
        self.tempo+=1
        if self.tempo > self.tempoColheita:
            self.fruta = Melancia(self.x, self.y, self.sala)

    def getFruit(self):
        if self.fruta != None:
            fruta = self.fruta
            self.fruta = None
            self.tempo = 0
            return fruta
        return None

    def render(self, screen):
        # desenha o chao
        cor = self.sala.cores[self.sala.bioma]

        pygame.draw.rect(screen, cor, pygame.Rect(self.x*self.escala, self.y*self.escala, self.escala, self.escala))

        # print desenha a arvore de melancia atraves do vetor pontos
        pygame.draw.polygon(screen, (0, 255, 0), self.pontos)


        # desenha flor
        if self.tempo > 2*self.tempoColheita//3 and self.tempo<=self.tempoColheita:
            pygame.draw.circle(screen, (255, 100, 254), (self.x*self.escala+self.escala*0.7, self.y*self.escala+self.escala*0.7), self.escala//7)
            (screen, (0, 110, 0), pygame.Rect(self.x*self.escala+19, self.y*self.escala+20, 16*self.escala//40, 20*self.escala//40))
        if self.fruta != None:
            self.fruta.render(screen)

        
