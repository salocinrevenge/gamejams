import pygame
import random
from excessoes.Win import Win
from chao import Chao
from parede import Parede
from algelin import norm
from barco import Barco
from bau import Bau
from pinguim import Pinguim
from programador import Programador

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
                if self.posBonus["B"] is not None and (x,y) == self.posBonus["B"] and self.bioma.lower() == "o":
                    entidades[-1][-1].append(Barco(self.bioma, x, y))
                if self.posBonus["E"] is not None and (x,y) in self.posBonus["E"] and self.bioma.lower() != "o": # spawnar entidades
                    if self.bioma.lower() == "a":
                        if random.random() < 0.9:
                            entidades[-1][-1].append(Pinguim(self.mundo,self, x, y))
                    if self.bioma.lower() == "d":
                        if random.random() < 0.1:
                            entidades[-1][-1].append(Pinguim(self.mundo,self, x, y))
        return entidades

    def carregarSala(self, arquivo):
        mapaOriginal = []
        mapaAtual = []
        
        self.posBonus = {"B":[], "E":[]}
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
                        case 'B':
                            objeto.append(Chao(self.bioma, x, y))
                            if self.bioma != self.bioma.lower(): # Se ele eh maiusculo
                                self.posBonus["B"].append((x,y))
                        case 'E':
                            objeto.append(Chao(self.bioma, x, y))
                            # if self.bioma != self.bioma.lower(): # Se ele eh maiusculo
                            self.posBonus["E"].append((x,y))
                        case 'C':
                            objeto.append(Chao(self.bioma, x, y))
                            if self.bioma != self.bioma.lower() and self.bioma.lower() != "o": # Se ele eh maiusculo
                                objeto.append(Bau(self.bioma, x, y))
                        case '#':
                            objeto.append(Chao(self.bioma, x, y))
                            objeto.append(Parede(self.bioma, x, y))
                    mapaOriginal[-1].append(objeto)
                    mapaAtual[-1].append(objeto)
        if len(self.posBonus["B"]) > 0:
            self.posBonus["B"] = random.choice(self.posBonus["B"])
        else:
            self.posBonus["B"] = None
            
        # for i in range(len(self.posBonus["E"])):
        #     if random.random() < 0.3: # 30% de chance de remover
        #         self.posBonus["E"].pop(i)
        
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
                for e in self.entidades[y][x]:
                    e.render(screen, camera, self.deslocamentoSala())    
                    
    def deslocamentoSala(self):
        return self.pos[0] * len(self.mapaAtual[0]), self.pos[1] * len(self.mapaAtual)
                    
    def adicionarPersonagem(self, personagem, posicao):
        personagem.setPos(posicao[0], posicao[1])
        self.entidades[posicao[1]][posicao[0]].append(personagem)
        
    def centro(self):
        return len(self.mapaAtual[0])//2, len(self.mapaAtual)//2
    
    def mover(self, objeto, x0, y0, x, y):
        dentro = True
        if x < 0 or x >= len(self.mapaAtual[0]):
            dentro = False
        if y < 0 or y >= len(self.mapaAtual):
            dentro = False
            
        if dentro:
            bloqueado = False
            for o in self.entidades[y][x]:
                if isinstance(o, Barco) and isinstance(objeto, Programador):
                    o.setNavegante(objeto)
                    self.entidades[y][x].remove(o)
                    continue
                bloqueado = True
                
            for o in self.mapaAtual[y][x]:
                if isinstance(o, Parede):
                    bloqueado = True
                if self.bioma.lower() == 'o' and isinstance(o, Chao):
                    if objeto.barco is None:
                        bloqueado = True
            
            if bloqueado:
                return False
            if x0 is not None and y0 is not None:
                self.entidades[y0][x0].remove(objeto)
            self.entidades[y][x].append(objeto)
            
            objeto.setPos(x, y)
            return True
        else:
            posSalaAlvo = [0,0]
            if x < 0:
                posSalaAlvo[0] = -1
            if x >= len(self.mapaAtual[0]):
                posSalaAlvo[0] = 1
            if y < 0:
                posSalaAlvo[1] = -1
            if y >= len(self.mapaAtual):
                posSalaAlvo[1] = 1
            posSalaAlvo[0] += self.pos[0]
            posSalaAlvo[1] += self.pos[1]
            if self.mundo.mover(objeto, posSalaAlvo, x%len(self.mapaAtual[0]), y%len(self.mapaAtual)):
                if x0 is not None and y0 is not None:
                    if objeto.barco is not None and self.mundo.salaAtual.bioma.lower() != 'o':
                        self.entidades[y0][x0].append(objeto.largarBarco())
                    self.entidades[y0][x0].remove(objeto)
                return True
            
        return False
    
    def interagir(self, personagem):
        pos = personagem.getPos()
        for elemento in self.mapaAtual[pos[1]][pos[0]]:
            if isinstance(elemento, Bau):
                personagem.inventario += elemento.abrir()
                return True
            
    def moverEntidade(self, entidade, x, y):
        pos = entidade.getPos()
        if self.mover(entidade, pos[0], pos[1], x, y):
            return True
        return False