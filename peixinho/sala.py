import pygame
from parede import Parede
from chao import Chao
from entidade import Entidade
import random
from melanceira import Melanceira
from ribopolho import Ribopolho
from excessoes.Win import Win
from foguete import Foguete

class Sala():
    def __init__(self, num, bioma, mundo) -> None:
        path = f"salas/sala{num}.txt"
        self.escala = self.getEscala(path)
        self.bioma = bioma
        self.mapaOriginal, self.mapaAtual = self.carregarSala(path)
        self.player = None
        self.mundo = mundo

    def getEscala(self, caminho):
        with open(caminho, "r") as arquivo:
            lines = arquivo.readlines()
            tamanho = len(lines)
        return 800//(tamanho)
    
    def removePlayer(self):
        self.mapaAtual[self.player.y][self.player.x] = self.mapaOriginal[self.player.y][self.player.x]
        self.player = None

    
    def setplayer(self, player):
        x, y = player.x, player.y
        self.player = player
        self.mapaAtual[y][x] = player

    probMela = {"I": 0, "U": 0,"S": 3,"P": 10,"F": 20,"R": 0,"M": 0,"D": 0 ,"O": 0,"B": 1}

    cores = {"I": (230,230,254), "U": (10,1,16),"S": (180,150,1),"P": (60,180,80),"F": (1,50,1),"R": (150,150,150),"M": (150,1,1),"D": (210,210,1),"O": (1,1,100),"B": (254,254,0)}

    def carregarSala(self, arquivo):
        mapaOriginal = []
        mapaAtual = []
        with open(arquivo, "r") as arquivo:
            for y, linha in enumerate(arquivo):
                linha = linha.strip()
                mapaOriginal.append([])
                mapaAtual.append([])
                for x, letra in enumerate(linha):
                    objeto = None
                    match letra:
                        case '#':
                            objeto = Parede(self.bioma, x, y, self.escala)
                        case '.':
                            if random.randint(0, 10000) < self.probMela[self.bioma]:
                                objeto = Melanceira(x, y, self)
                            else:
                                objeto = Chao(self.bioma, x, y, self.escala)
                    mapaOriginal[-1].append(objeto)
                    mapaAtual[-1].append(objeto)
        
        return mapaOriginal, mapaAtual


    def mover(self, objeto, x, y):

        if x < 0 or y < 0 or x >= len(self.mapaAtual[0]) or y >= len(self.mapaAtual):
            if x < 0:
                novoX, novoY = len(self.mapaAtual[0])-1, objeto.y
                mover = (-1,0)
            if y < 0:
                novoX, novoY = objeto.x, len(self.mapaAtual)-1
                mover = (0,-1)
            if x >= len(self.mapaAtual[0]):
                novoX, novoY = 0, objeto.y
                mover = (1,0)
            if y >= len(self.mapaAtual):
                novoX, novoY = objeto.x, 0
                mover = (0,1)

            x, y = objeto.x, objeto.y
            objeto.x = novoX
            objeto.y = novoY
            
            if self.mundo.mover(*mover):
                self.mapaAtual[y][x] = self.mapaOriginal[y][x]
                return
            else:
                objeto.x , objeto.y = x, y
            return

        if type(self.mapaAtual[y][x]) in {Chao, Melanceira, Foguete}:
            self.mapaAtual[objeto.y][objeto.x] = self.mapaOriginal[objeto.y][objeto.x]
            self.mapaAtual[y][x] = objeto
            objeto.x = x
            objeto.y = y

    def colocar(self, x, y, objeto):
        if isinstance(self.mapaOriginal[y][x], Chao):
            self.mapaOriginal[y][x] = objeto
            objeto.atualizarPosicao(x, y, self)
            return True
        return False

    def tick(self):
        if self.player:
            self.player.tick()
        # random tick
        i,j = random.randint(0, len(self.mapaAtual)-1), random.randint(0, len(self.mapaAtual[0])-1)
        self.mapaAtual[i][j].tick()

    def input(self, evento):
        if self.player:
            self.player.input(evento)

    def plantar(self, x, y):
        if isinstance(self.mapaAtual[y][x], Ribopolho):
            if isinstance(self.mapaOriginal[y][x], Chao) and self.mapaOriginal[y][x].bioma in {"S", "P", "F", "M"}:
                self.mapaOriginal[y][x] = Melanceira(x, y, self, 30)
                if self.bioma == "M":
                    raise Win("EBA! Marte eh habitavel!")
                return True
        return False

    def render(self, screen):
        # desenha a borda da sala
        pygame.draw.rect(screen, (255, 60, 60), pygame.Rect(0, 0, 800, 800), 2)
        for i in range(len(self.mapaAtual)):
            for j in range(len(self.mapaAtual[i])):
                objeto = self.mapaAtual[i][j]
                # verifica se o objeto é uma entidade
                if isinstance(objeto, Entidade):
                    self.mapaOriginal[i][j].render(screen)
                objeto.render(screen)
