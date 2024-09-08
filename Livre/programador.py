import pygame

from personagem import Personagem

class Programador(Personagem):
    def __init__(self, x, y, mundo) -> None:
        super().__init__(x, y, mundo)
        self.imagem = pygame.image.load("assets/programador.png")
        self.mundo = mundo
        self.demanda = None
        self.velX = 0
        self.velY = 0
        self.intervaloPassosMax = 7
        self.intervaloPassos = 0
        
    def tick(self):
        self.intervaloPassos -= 1
        if self.intervaloPassos <= 0:
            self.mover(self.velX, self.velY)
            
        if self.demanda:
            dx, dy = self.demanda
            self.mundo.salaAtual.mover(self, self.x, self.y, self.x+dx, self.y+dy)
            self.demanda = None
        super().tick()

    
    def render(self, screen, camera, deslocamento):
        camera.render(screen, self.imagem, (self.x+deslocamento[0], self.y+deslocamento[1]))
        super().render(screen, camera, deslocamento)
        
    def mover(self, dx, dy):
        self.demanda = (dx, dy)
        self.intervaloPassos = self.intervaloPassosMax
        
    def limitarVelocidade(self):
        if self.velX > 1:
            self.velX = 1
        if self.velX < -1:
            self.velX = -1
        if self.velY > 1:
            self.velY = 1
        if self.velY < -1:
            self.velY = -1
        
    def input(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_w or evento.key == pygame.K_UP:
                self.velY -= 1
                self.limitarVelocidade()
            if evento.key == pygame.K_s or evento.key == pygame.K_DOWN:
                self.velY += 1
                self.limitarVelocidade()
            if evento.key == pygame.K_a or evento.key == pygame.K_LEFT:
                self.velX -= 1
                self.limitarVelocidade()
            if evento.key == pygame.K_d or evento.key == pygame.K_RIGHT:
                self.velX += 1
                self.limitarVelocidade()
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_w or evento.key == pygame.K_UP:
                self.velY += 1
                self.limitarVelocidade()
            if evento.key == pygame.K_s or evento.key == pygame.K_DOWN:
                self.velY -= 1
                self.limitarVelocidade()
            if evento.key == pygame.K_a or evento.key == pygame.K_LEFT:
                self.velX += 1
                self.limitarVelocidade()
            if evento.key == pygame.K_d or evento.key == pygame.K_RIGHT:
                self.velX -= 1
                self.limitarVelocidade()