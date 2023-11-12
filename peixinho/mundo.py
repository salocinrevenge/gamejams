import pygame
from sala import Sala
import random
from ribopolho import Ribopolho
from excessoes.Die import Die
from foguete import Foguete
from chao import Chao

class Mundo():
    def __init__(self) -> None:
        self.mapaOriginal, self.mapaAtual = self.carregarSala("salas/mundo.txt")
        self.salas = self.criarSalas()
        self.atual = (9,9) # i,j
        self.contadorObjetivo = 0
        self.mostrarMundo = False
        self.escala = 800//(len(self.mapaOriginal)*2)
        self.player = Ribopolho(9, 9 ,self.salas[self.atual[0]][self.atual[1]])
        self.salas[self.atual[0]][self.atual[1]].setplayer(self.player)

        self.salas[17][0].mapaOriginal[9][9] = Foguete(9, 9, self.salas[17][0])
        self.salas[17][0].mapaAtual[9][9] = self.salas[17][0].mapaOriginal[9][9]

    def criarSalas(self):
        salas = []
        for i in range(len(self.mapaAtual)):
            salas.append([])
            for j in range(len(self.mapaAtual[i])):
                salas[-1].append(Sala(random.randint(0,9), self.mapaOriginal[i][j], self)) # sorteia de 0 a 9
                # salas[-1].append(Sala(0, self.mapaOriginal[i][j], self)) # sorteia de 0 a 9
        return salas

    def decolar(self):
        foguete = self.salas[self.atual[0]][self.atual[1]].mapaOriginal[self.player.y][self.player.x]
        self.salas[self.atual[0]][self.atual[1]].mapaOriginal[self.player.y][self.player.x] = Chao(self.player.sala.bioma, self.player.x, self.player.y, self.player.sala.escala)
        self.player.sala.removePlayer()
        self.player.foguete = foguete
        i = self.atual[0]
        salaAlvo = self.salas[i][self.atual[1]]
        while salaAlvo.bioma != "U":
            i-=1
            salaAlvo = self.salas[i][self.atual[1]]
        self.atual = (i, self.atual[1])
        self.salas[self.atual[0]][self.atual[1]].setplayer(self.player)
        self.player.sala = self.salas[self.atual[0]][self.atual[1]]


    def mover(self, dx, dy):
        if self.atual[1]+dx < 0 or self.atual[0]+dy < 0 or self.atual[1]+dx >= len(self.salas) or self.atual[0]+dy >= len(self.salas[0]):
            return False
        if self.salas[self.atual[0]+dy][self.atual[1]+dx].bioma == "U" and self.salas[self.atual[0]][self.atual[1]].bioma != "U":
            return False
        self.atual = (self.atual[0]+dy, self.atual[1]+dx)
        self.salas[self.atual[0]][self.atual[1]].setplayer(self.player)
        self.player.sala = self.salas[self.atual[0]][self.atual[1]]
        if self.player.sala.bioma == "M":
            self.player.sala.mapaOriginal[self.player.y][self.player.x] = self.player.foguete
            self.player.foguete.atualizarPosicao(self.player.x, self.player.y, self.player.sala)
            self.player.foguete = None
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
        try:
            self.salas[self.atual[0]][self.atual[1]].tick()
        except Die:
            self.salas[self.atual[0]][self.atual[1]].removePlayer()
            self.atual = (9,9)
            self.player = Ribopolho(9, 9 ,self.salas[self.atual[0]][self.atual[1]])
            self.salas[self.atual[0]][self.atual[1]].setplayer(self.player)
        self.contadorObjetivo += 0.001

    cores = {"I": (230,230,255), "U": (30,0,40),"S": (180,150,0),"P": (100,235,100),"F": (0,50,0),"R": (150,150,150),"M": (150,0,0),"D": (255,255,0),"O": (0,0,100),"B": (255,255,0)}

    def input(self, evento):
        # verifica se botao m foi pressionado
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_m:
                self.contadorObjetivo = 0
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
        # desenha o objetivo como circulo vazio
        if self.contadorObjetivo > 0.04:
            pygame.draw.circle(screen, (255, 0, 0), (604, 231), 20, 5)
    def render(self, screen):
        # desenha a borda da sala
        self.salas[self.atual[0]][self.atual[1]].render(screen)
        if self.mostrarMundo:
            self.renderMundo(screen)
            