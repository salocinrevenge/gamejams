from excessoes.Die import Die
import pygame
from entidade import Entidade

class Ribopolho(Entidade):
    # Repolho de perna de hipopotamo
    def __init__(self, x, y, sala, vidaMaxima = 10000): # 10000 = 2m 45s
        self.x = x
        self.y = y
        self.vidaMaxima = vidaMaxima
        self.vida = vidaMaxima
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

        # folhas
        # vvvv                              x  y  raioLargura raioAltura  anguloInicial anguloFinal   larguraDaLinha
        pygame.draw.arc(screen, (0, 0, 0), (x-(raio*5/20), y+(raio*14/20), raio*1.6, raio*1.4), -(3.14*0.45), (3.14*0.74), (raio*2//20)) 
        pygame.draw.arc(screen, (0, 0, 0), (x+(raio*15/20), y+(raio*4/20), raio*1.6, raio*1.4), (3.14*0.45), (3.14*0.9), (raio*2//20)) 
        pygame.draw.arc(screen, (0, 0, 0), (x-(raio*2/20), y+(raio*4/20), raio*1.6, raio*1.4), (3.14*0.30), (3.14*0.64), (raio*2//20)) 
        
        # olhos
        pygame.draw.circle(screen, (255, 255, 255), (x+(raio*13/20), y+(raio*23/20)), (raio*7/20))
        pygame.draw.circle(screen, (0, 0, 0), (x+(raio*10/20), y+(raio*23/20)), (raio*6/20))
        pygame.draw.circle(screen, (255, 255, 255), (x+(raio*10/20), y+(raio*21/20)), (raio*2/20))

        pygame.draw.circle(screen, (255, 255, 255), (x+(raio*33/20), y+(raio*23/20)), (raio*7/20))
        pygame.draw.circle(screen, (0, 0, 0), (x+(raio*36/20), y+(raio*23/20)), (raio*6/20))
        pygame.draw.circle(screen, (255, 255, 255), (x+(raio*36/20), y+(raio*21/20)), (raio*2/20))

        # boca feliz
        pygame.draw.arc(screen, (0, 0, 0), (x+(raio*18/20), y+(raio*28/20), raio*0.5, raio*0.5), (3.14*0.9), (3.14*0.1), (raio*2//20))


    def desenhaPernas(self, screen, x, y, raio):
        # pernas
        pygame.draw.rect(screen, (120, 120, 120), pygame.Rect(x+(raio*5/20), y+(raio*20/20), raio*0.5, raio*1.5))
        pygame.draw.rect(screen, (120, 120, 120), pygame.Rect(x+(raio*25/20), y+(raio*20/20), raio*0.5, raio*1.5))
        # unhas
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x+(raio*8/20), y+(raio*45/20), raio*0.3, raio*0.2))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x+(raio*28/20), y+(raio*45/20), raio*0.3, raio*0.2))

    def desenhaHUD(self, screen, x, y):
        # regiao
        pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(x, y, 800, 100), border_radius=25)
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x, y, 800, 100), 2, border_radius=25)

        # vida
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x+20, y+20, 300, 60), border_radius=2)
        pct = self.vida/self.vidaMaxima
        pygame.draw.rect(screen, (255*(1-pct), 255*pct, 0), pygame.Rect(x+20, y+20, 300*pct, 60), border_radius=2)

    def render(self, screen):
        raio = 16
        self.desenhaPernas(screen, self.x*self.escala, self.y*self.escala, raio)
        self.desenhaCabeca(screen, self.x*self.escala, self.y*self.escala, raio)
        self.desenhaHUD(screen, 0,800)


    def tick(self):
        self.vida -= 1
        if self.vida <= 0:
            raise Die("Ribopolho morreu de velhice")
        
    

    