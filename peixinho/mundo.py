import pygame
from sala import Sala
import random
from ribopolho import Ribopolho

class Mundo():
    def __init__(self) -> None:
        self.mapaOriginal, self.mapaAtual = self.carregarSala("salas/mundo.txt")
        self.salas = self.criarSalas()
        self.atual = (9,9) # i,j
        self.mostrarMundo = False
        self.escala = 800//(len(self.mapaOriginal)*2)
        self.player = Ribopolho(self.atual[0], self.atual[1] ,self.salas[self.atual[0]][self.atual[1]])
        self.salas[self.atual[0]][self.atual[1]].setplayer(self.player)

    def criarSalas(self):
        salas = []
        for i in range(len(self.mapaAtual)):
            salas.append([])
            for j in range(len(self.mapaAtual[i])):
                salas[-1].append(Sala(random.randint(0,9), self.mapaOriginal[i][j], self)) # sorteia de 0 a 9
                # salas[-1].append(Sala(0, self.mapaOriginal[i][j], self)) # sorteia de 0 a 9
        return salas

    def mover(self, dx, dy):
        if self.atual[1]+dx < 0 or self.atual[0]+dy < 0 or self.atual[1]+dx >= len(self.salas) or self.atual[0]+dy >= len(self.salas[0]):
            return False
        self.atual = (self.atual[0]+dy, self.atual[1]+dx)
        self.salas[self.atual[0]][self.atual[1]].setplayer(self.player)
        self.player.sala = self.salas[self.atual[0]][self.atual[1]]
        return True

    def carregarSala(self, arquivo):
        mapaOriginal = []
        mapaAtual = []
        with open(arquivo, "r") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                mapaOriginal.append(list(linha))
                mapaAtual.append(list(linha))
        return mapaOriginal, mapaAtual

    def tick(self):
        self.salas[self.atual[0]][self.atual[1]].tick()

    cores = {"I": (230,230,255), "U": (30,0,40),"S": (180,150,0),"P": (100,235,100),"F": (0,50,0),"R": (150,150,150),"M": (150,0,0),"D": (255,255,0),"O": (0,0,100),"B": (255,255,0)}

    def input(self, evento):
        # verifica se botao m foi pressionado
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_m:
                self.mostrarMundo = True
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_m:
                self.mostrarMundo = False
        self.salas[self.atual[0]][self.atual[1]].input(evento)
    
    def renderMundo(self, screen):
        for linha in range(len(self.mapaAtual)):
            for coluna in range(len(self.mapaAtual[linha])):
                bioma = self.mapaOriginal[linha][coluna]
                pygame.draw.rect(screen, self.cores[bioma], pygame.Rect(coluna*self.escala+220, linha*self.escala+220, self.escala, self.escala))
        # desenha o player
        self.player.desenhaCabeca(screen, self.atual[1]*self.escala+220, self.atual[0]*self.escala+220, 10)

    def render(self, screen):
        # desenha a borda da sala
        self.salas[self.atual[0]][self.atual[1]].render(screen)
        if self.mostrarMundo:
            self.renderMundo(screen)
            