import pygame
from sala import Sala
import random

class Mundo():
    def __init__(self) -> None:
        self.mapaOriginal, self.mapaAtual = self.carregarSala("salas/mundo.txt")
        self.salas = self.criarSalas()

    def tick(self):
        pass
    def input(self, evento):
        pass
    
    def render(self, screen):
        pass
    
    
    def criarSalas(self):
        salas = []
        for i in range(len(self.mapaAtual)):
            salas.append([])
            for j in range(len(self.mapaAtual[i])):
                salas[-1].append(Sala(random.randint(0,0), self.mapaOriginal[i][j], self)) # sorteia de 0 a 9
        return salas

    def carregarSala(self, arquivo):
        mapaOriginal = []
        mapaAtual = []
        with open(arquivo, "r") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                mapaOriginal.append(list(linha))
                mapaAtual.append(list(linha))
        return mapaOriginal, mapaAtual
        
            