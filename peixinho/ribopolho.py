from excessoes.Die import Die
import pygame
from entidade import Entidade

class Ribopolho(Entidade):
    # Repolho de perna de hipopotamo
    def __init__(self, x, y, sala, tempoDeVida = 100000):
        self.x = x
        self.y = y
        self.tempoDeVida = tempoDeVida
        self.sala = sala
        self.escala = sala.escala
    
    def input(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_a or evento.key == pygame.K_LEFT:
                self.move(-1, 0)
            if evento.key == pygame.K_d or evento.key == pygame.K_RIGHT:
                self.move(1, 0)
            if evento.key == pygame.K_w or evento.key == pygame.K_UP:
                self.move(0, -1)
            if evento.key == pygame.K_s or evento.key == pygame.K_DOWN:
                self.move(0, 1)
        
    
    def move(self, dx, dy):
        self.sala.mover(self, self.x+dx, self.y+dy)

    def desenhaCabeca(self, screen, x, y, raio):
        # desenha cabeca
        pygame.draw.circle(screen, (0, 255, 0), (x+raio, y+raio), raio)

    def render(self, screen):
        # desneha circulo verde
        raio = 20
        self.desenhaCabeca(screen, self.x*self.escala, self.y*self.escala, raio)

    def tick(self):
        self.tempoDeVida -= 1
        if self.tempoDeVida <= 0:
            raise Die("Ribopolho morreu de velhice")
    

    