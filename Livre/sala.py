import pygame
import random
from excessoes.Win import Win
from chao import Chao
from parede import Parede

class Sala():
    def __init__(self, num, bioma, mundo) -> None:
        path = f"salas/sala{num}.txt"
        self.bioma = bioma
        self.mapaOriginal, self.mapaAtual = self.carregarSala(path)
        self.mundo = mundo
        self.entidades = self.spawnEntidades()
        
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
        pass

    def input(self, evento):
        for y, linha in enumerate(self.entidades):
            for x, objeto in enumerate(linha):
                for o in objeto:
                    o.input(evento)

    def render(self, screen, camera):
        for y, linha in enumerate(self.mapaAtual):
            for x, objeto in enumerate(linha):
                for o in objeto:
                    o.render(screen,camera)
        for y, linha in enumerate(self.entidades):
            for x, objeto in enumerate(linha):
                for o in objeto:
                    o.render(screen, camera)
                    
    def adicionarPersonagem(self, personagem, posicao):
        personagem.setPos(posicao[0], posicao[1])
        self.entidades[posicao[1]][posicao[0]].append(personagem)
        
    def centro(self):
        return len(self.mapaAtual[0])//2, len(self.mapaAtual)//2