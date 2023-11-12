import pygame
from parede import Parede
from chao import Chao
from entidade import Entidade

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
    
    def setplayer(self, player):
        x, y = player.x, player.y
        self.player = player
        self.mapaAtual[y][x] = player

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
            else:
                objeto.x , objeto.y = x, y
            return

        if type(self.mapaAtual[y][x]) == Chao:
            self.mapaAtual[objeto.y][objeto.x] = self.mapaOriginal[objeto.y][objeto.x]
            self.mapaAtual[y][x] = objeto
            objeto.x = x
            objeto.y = y

    def tick(self):
        if self.player:
            self.player.tick()

    def input(self, evento):
        if self.player:
            self.player.input(evento)

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
