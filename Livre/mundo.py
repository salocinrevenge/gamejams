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
        self.salaAtual.input(evento)
    
    def render(self, screen):
        self.salaAtual.render(screen, self.camera)
    
    
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
        
            