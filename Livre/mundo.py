import pygame
from sala import Sala
import random
from camera import Camera
from programador import Programador

class Mundo():
    def __init__(self) -> None:
        self.mapaOriginal, self.mapaAtual = self.carregarSala("salas/mundo.txt")
        self.salas = self.criarSalas()
        self.salaAtual = self.salas[0][0]
        self.camera = Camera(self, (250,250))
        self.programador = Programador(0,0, self)
        self.salaAtual.adicionarPersonagem(self.programador, self.salaAtual.centro())

    def tick(self):
        self.camera.tick()
        self.salaAtual.tick()
        
    def input(self, evento):
        posCentral = self.salaAtual.getPos()
        for i in range(-1,2):
            for j in range(-1,2):
                self.salas[i+posCentral[0]][j+posCentral[1]].input(evento)
    
    def render(self, screen):
        posCentral = self.salaAtual.getPos()
        for i in range(-1,2):
            for j in range(-1,2):
                self.salas[i+posCentral[0]][j+posCentral[1]].render(screen, self.camera)
    
    
    def criarSalas(self):
        salas = []
        for i in range(len(self.mapaAtual)):
            salas.append([])
            for j in range(len(self.mapaAtual[i])):
                salas[-1].append(Sala(random.randint(0,0), self.mapaOriginal[i][j], self, (i,j))) # sorteia de 0 a 9
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
    
    def mover(self, personagem, posSalaAlvo, x, y):
        if posSalaAlvo[0] < 0 or posSalaAlvo[0] >= len(self.salas) or posSalaAlvo[1] < 0 or posSalaAlvo[1] >= len(self.salas[0]):
            return False
        if self.salas[posSalaAlvo[0]][posSalaAlvo[1]].mover(personagem, None, None, x, y):
            return True
            