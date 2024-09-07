import pygame
import random
from excessoes.Win import Win
from chao import Chao

class Sala():
    def __init__(self, num, bioma, mundo) -> None:
        path = f"salas/sala{num}.txt"
        self.bioma = bioma
        self.mapaOriginal, self.mapaAtual = self.carregarSala(path)
        self.mundo = mundo

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
                            pass
                    mapaOriginal[-1].append(objeto)
                    mapaAtual[-1].append(objeto)
        
        return mapaOriginal, mapaAtual


    def tick(self):
        pass

    def input(self, evento):
        pass

    def render(self, screen, camera):
        for y, linha in enumerate(self.mapaAtual):
            for x, objeto in enumerate(linha):
                for o in objeto:
                    o.render(screen,camera)