import pygame
import random
from excessoes.Win import Win
from chao import Chao
from parede import Parede
from algelin import norm

class Sala():
    def __init__(self, num, bioma, mundo, pos) -> None:
        path = f"salas/sala{num}.txt"
        self.pos = pos
        self.bioma = bioma
        self.mapaOriginal, self.mapaAtual = self.carregarSala(path)
        self.mundo = mundo
        self.entidades = self.spawnEntidades()
        
    def getPos(self):
        return self.pos
        
    def spawnEntidades(self):
        entidades = []
        for y, linha in enumerate(self.mapaAtual):
            entidades.append([])
            for x, objeto in enumerate(linha):
                entidades[-1].append([])
        return entidades

    def carregarSala(self, arquivo):
        mapaOriginal = []
        mapaAtual = []
        with open(arquivo, "r") as arquivo:
            for y, linha in enumerate(arquivo):
                linha = linha.strip()
                mapaOriginal.append([])
                mapaAtual.append([])
                for x, letra in enumerate(linha):
                    objeto = []
                    match letra:
                        case '.':
                            objeto.append(Chao(self.bioma, x, y))
                        case '#':
                            objeto.append(Chao(self.bioma, x, y))
                            objeto.append(Parede(self.bioma, x, y))
                    mapaOriginal[-1].append(objeto)
                    mapaAtual[-1].append(objeto)
        
        return mapaOriginal, mapaAtual


    def tick(self):
        for y, linha in enumerate(self.entidades):
            for x, objeto in enumerate(linha):
                for o in objeto:
                    o.tick()

    def input(self, evento):
        for y, linha in enumerate(self.entidades):
            for x, objeto in enumerate(linha):
                for o in objeto:
                    o.input(evento)

    def render(self, screen, camera):
        for y, linha in enumerate(self.mapaAtual):
            for x, objeto in enumerate(linha):
                for o in objeto:
                    o.render(screen,camera, self.deslocamentoSala())
        for y, linha in enumerate(self.entidades):
            for x, objeto in enumerate(linha):
                for o in objeto:
                    o.render(screen, camera, self.deslocamentoSala())
                    
    def deslocamentoSala(self):
        return self.pos[0] * len(self.mapaAtual[0]), self.pos[1] * len(self.mapaAtual)
                    
    def adicionarPersonagem(self, personagem, posicao):
        personagem.setPos(posicao[0], posicao[1])
        self.entidades[posicao[1]][posicao[0]].append(personagem)
        
    def centro(self):
        return len(self.mapaAtual[0])//2, len(self.mapaAtual)//2
    
    def mover(self, objeto, x0, y0, x, y):
        dentro = True
        print(x, y)
        if x < 0 or x >= len(self.mapaAtual[0]):
            dentro = False
        if y < 0 or y >= len(self.mapaAtual):
            dentro = False
            
        print(dentro)
        if dentro:
            bloqueado = False
            for o in self.entidades[y][x]:
                bloqueado = True
                
            for o in self.mapaAtual[y][x]:
                if isinstance(o, Parede):
                    bloqueado = True
            
            print(f"{bloqueado=}")
            if bloqueado:
                return
            
            if x0 and y0:
                print(f"{x0=}, {y0=}, removendo {objeto} de {self.entidades[y0][x0]}")
                self.entidades[y0][x0].remove(objeto)
            print(f"Agora esta assim: {self.entidades[y][x]}")
            self.entidades[y][x].append(objeto)
            
            objeto.setPos(x, y)
            return
        else:
            posSalaAlvo = (int(self.pos[0]+norm(y)), int(self.pos[1]+norm(x)))
            print(posSalaAlvo)
            if self.mundo.mover(objeto, posSalaAlvo, x%len(self.mapaAtual[0]), y%len(self.mapaAtual)):
                if x0 and y0:
                    self.entidades[y0][x0].remove(objeto)