from excessoes.Die import Die
import pygame
from entidade import Entidade
from melanceira import Melanceira
from melancia import Melancia
from semente import Semente
from foguete import Foguete
from chao import Chao

class Ribopolho(Entidade):
    # Repolho de perna de hipopotamo
    def __init__(self, x, y, sala, vidaMaxima = 2500): # 10000 = 2m 45s, 5000 = 1m 22s, 2500 = 41s
        self.x = x
        self.y = y
        self.vidaMaxima = vidaMaxima
        self.vida = vidaMaxima
        self.sala = sala
        self.escala = sala.escala
        self.selecao = 0
        self.bolsa = [None, None, None, None, None, None, None]
        self.foguete = None
    
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
            if evento.key == pygame.K_SPACE:
                self.interact()
            if evento.key == pygame.K_q:
                if len(self.bolsa) > 0:
                    self.selecao = (self.selecao-1)%len(self.bolsa)
            if evento.key == pygame.K_e:
                if len(self.bolsa) > 0:
                    self.selecao = (self.selecao+1)%len(self.bolsa)
            
    def clamp(self, valor, minimo, maximo):
        return max(min(valor, maximo), minimo)

    def interact(self):
        if self.bolsa[self.selecao] == None:
            objetoMapa = self.sala.mapaOriginal[self.y][self.x]
            if isinstance(objetoMapa, Melanceira):
                fruta = objetoMapa.getFruit()
                if fruta != None:
                    self.bolsa[self.selecao] = fruta
            elif isinstance(objetoMapa, Foguete):
                self.bolsa[self.selecao] = objetoMapa
                self.sala.mapaOriginal[self.y][self.x] = Chao(self.sala.bioma, self.x, self.y, self.sala.escala)
            return
        if isinstance(self.bolsa[self.selecao], Melancia):
            if isinstance(self.sala.mapaOriginal[self.y][self.x], Foguete):
                self.bolsa[self.selecao] = None
                self.sala.mundo.decolar()
                return
            vida, semente = self.bolsa[self.selecao].comer()
            self.vida = self.clamp (self.vida+ vida, 0, self.vidaMaxima)
            self.bolsa[self.selecao] = semente
            return

        if isinstance(self.bolsa[self.selecao], Semente):
            if self.sala.plantar(self.x, self.y):
                self.bolsa[self.selecao] = None
            return
        
        if isinstance(self.bolsa[self.selecao], Foguete):
            if self.sala.bioma == "R":
                if self.sala.colocar(self.x, self.y, self.bolsa[self.selecao]):
                    self.bolsa[self.selecao] = None
            return



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

        # bolsa
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x+350 + self.selecao*60, y+20, 60, 60), 2, border_radius=2)
        for i in range(len(self.bolsa)):
            if self.bolsa[i] != None:
                self.bolsa[i].renderItem(screen, x+350 + i*60+8, y+20+3, 2.6)

    def render(self, screen):
        self.desenhaHUD(screen, 0,800)
        if self.foguete == None:
            raio = 16
            self.desenhaPernas(screen, self.x*self.escala, self.y*self.escala, raio)
            self.desenhaCabeca(screen, self.x*self.escala, self.y*self.escala, raio)
        else:
            self.foguete.atualizarPosicao(self.x, self.y, self.sala)
            self.foguete.render(screen)


    def tick(self):
        self.vida = self.clamp(self.vida-1, 0, self.vidaMaxima)
        if self.vida == 0:
            raise Die("Ribopolho morreu de velhice")
        
    

    