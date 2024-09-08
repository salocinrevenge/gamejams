import pygame
import random
from personagem import Personagem
import random

class Inimigo(Personagem):
    
    imagem = {"frente": pygame.image.load("assets/computer.png")}
    def __init__(self, mundo, sala, x, y) -> None:
        super().__init__(x, y, mundo)
        self.mundo = mundo
        self.x = x
        self.y = y
        self.sala = sala
        self.intervaloPassosMax = 5
        self.demanda = (0, 0)
        self.plano = []
        self.jogador = None
        self.dano = 10
        self.tempoDanoMax = 50
        self.tempoDano = 0
        


    def render(self, screen, camera, deslocamento):
        camera.render(screen, self.imagem["frente"], (self.x+deslocamento[0], self.y+deslocamento[1]))
        super().render(screen, camera, deslocamento)
        
    acoes = ["a", "d", "w", "s"]
    pos = {"a": (-1, 0), "d": (1, 0), "w": (0, -1), "s": (0, 1)}
        
    def distPlayer(self, aditive, jogador):
        posSalaJogador = self.mundo.salaAtual.getRealPos()
        xjreal, yjreal = jogador.x +posSalaJogador[0] , jogador.y+posSalaJogador[1]
        posSala = self.sala.getRealPos()
        xreal, yreal = self.x + posSala[0], self.y + posSala[1]
        
        return abs(xjreal-(xreal+aditive[0])) + abs(yjreal-(yreal+aditive[1]))
        
    def minimizar(self, acoes, jogador):
        melhor = float("inf")
        melhorAcao = None
        
        for acao in acoes:
            dx, dy = self.pos[acao]
            dist = self.distPlayer((dx, dy), jogador)
            if dist < melhor:
                melhor = dist
                melhorAcao = acao
        return self.pos[melhorAcao]
        
    def think(self):
        jog = self.mundo.programador
        if self.intervaloPassos <= 0:
            if random.random() < 0.1:
                if random.random() < 0.4:
                    self.demanda = self.pos[random.choice(self.acoes)]
                else:
                    self.demanda = self.minimizar(self.acoes, jog)
                self.intervaloPassos = self.intervaloPassosMax

    def tick(self):
        self.intervaloPassos -= 1
        self.tempoDano -= 1
        if self.distPlayer((0, 0), self.mundo.programador) < 2 and self.tempoDano <= 0:
            self.mundo.programador.vidaUpdate(-self.dano)
            self.tempoDano = self.tempoDanoMax
        self.think()
        if self.demanda:
            self.sala.moverEntidade(self, self.x+self.demanda[0], self.y+self.demanda[1])
            self.demanda = None
        
        super().tick()
