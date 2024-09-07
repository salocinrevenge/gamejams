import pygame

from personagem import Personagem

class Programador(Personagem):
    def __init__(self, x, y, mundo) -> None:
        super().__init__(x, y, mundo)
        self.imagem = pygame.image.load("assets/programador.png")
        self.mundo = mundo
        self.demanda = None

    def tick(self):
        if self.demanda:
            dx, dy = self.demanda
            self.mundo.salaAtual.mover(self, self.x, self.y, self.x+dx, self.y+dy)
            self.demanda = None

    
    def render(self, screen, camera, deslocamento):
        camera.render(screen, self.imagem, (self.x+deslocamento[0], self.y+deslocamento[1]))
        
    def mover(self, dx, dy):
        self.demanda = (dx, dy)
        
    def input(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_w or evento.key == pygame.K_UP:
                self.mover(0,-1)
            if evento.key == pygame.K_s or evento.key == pygame.K_DOWN:
                self.mover(0,1)
            if evento.key == pygame.K_a or evento.key == pygame.K_LEFT:
                self.mover(-1,0)
            if evento.key == pygame.K_d or evento.key == pygame.K_RIGHT:
                self.mover(1,0)