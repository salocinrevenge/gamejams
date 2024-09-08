import pygame
from sala import Sala
import random
from camera import Camera
from programador import Programador

class Mundo():
    def __init__(self) -> None:
        self.mapaOriginal, self.mapaAtual = self.carregarSala("salas/mundo.txt")
        self.salas = self.criarSalas()
        self.salaAtual = self.salas[self.centro()[0]][self.centro()[1]]
        self.camera = Camera(self, (250,250))
        self.programador = Programador(self.salaAtual.pos[0],self.salaAtual.pos[1], self)
        self.camera.setTarget(self.programador)
        self.salaAtual.adicionarPersonagem(self.programador, self.salaAtual.centro())
        self.renderDistance = 3

    def centro(self):
        return (len(self.salas)//2, len(self.salas[0])//2)

    def tick(self):
        posCentral = self.salaAtual.getPos()
        for i in range(-self.renderDistance,self.renderDistance+1):
            for j in range(-self.renderDistance,self.renderDistance+1):
                if i+posCentral[0] < 0 or i+posCentral[0] >= len(self.salas) or j+posCentral[1] < 0 or j+posCentral[1] >= len(self.salas[0]):
                    continue
                self.salas[i+posCentral[0]][j+posCentral[1]].tick()
        self.camera.tick()
        
    def input(self, evento):
        posCentral = self.salaAtual.getPos()
        for i in range(-self.renderDistance,self.renderDistance+1):
            for j in range(-self.renderDistance,self.renderDistance+1):
                if i+posCentral[0] < 0 or i+posCentral[0] >= len(self.salas) or j+posCentral[1] < 0 or j+posCentral[1] >= len(self.salas[0]):
                    continue
                self.salas[i+posCentral[0]][j+posCentral[1]].input(evento)
    
    def render(self, screen):
        posCentral = self.salaAtual.getPos()
        for i in range(-self.renderDistance,self.renderDistance+1):
            for j in range(-self.renderDistance,self.renderDistance+1):
                if i+posCentral[0] < 0 or i+posCentral[0] >= len(self.salas) or j+posCentral[1] < 0 or j+posCentral[1] >= len(self.salas[0]):
                    continue
                self.salas[i+posCentral[0]][j+posCentral[1]].render(screen, self.camera)
    
    
    def criarSalas(self):
        salas = []
        for i in range(len(self.mapaAtual)):
            salas.append([])
            for j in range(len(self.mapaAtual[i])):
                salas[-1].append(Sala(random.randint(0,1), self.mapaOriginal[i][j], self, (i,j))) # sorteia de 0 a 9
        return salas

    def carregarSala(self, arquivo):
        mapaOriginal = []
        mapaAtual = []
        with open(arquivo, "r") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                mapaOriginal.append(list(linha))
                mapaAtual.append(list(linha))
                
        # transpoe o mapa
        mapaOriginal = [list(x) for x in zip(*mapaOriginal)]
        mapaAtual = [list(x) for x in zip(*mapaAtual)]
        
        return mapaOriginal, mapaAtual
    
    def mover(self, personagem, posSalaAlvo, x, y):
        if posSalaAlvo[0] < 0 or posSalaAlvo[0] >= len(self.salas) or posSalaAlvo[1] < 0 or posSalaAlvo[1] >= len(self.salas[0]):
            return False
        if self.salas[posSalaAlvo[0]][posSalaAlvo[1]].mover(personagem, None, None, x, y):
            self.salaAtual = self.salas[posSalaAlvo[0]][posSalaAlvo[1]]
            return True
        return False
            