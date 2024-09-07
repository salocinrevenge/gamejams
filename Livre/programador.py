import pygame

from personagem import Personagem

class Programador(Personagem):
    def __init__(self, x, y, mundo) -> None:
        super().__init__(x, y, mundo)
        self.imagem = pygame.image.load("assets/programador.png")

    def tick(self):
        pass
    
    def render(self, screen, camera):
        camera.render(screen, self.imagem, (self.x, self.y))
        
    def input(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_w or evento.key == pygame.K_UP:
                self.y -= 1
            if evento.key == pygame.K_s or evento.key == pygame.K_DOWN:
                self.y += 1
            if evento.key == pygame.K_a or evento.key == pygame.K_LEFT:
                self.x -= 1
            if evento.key == pygame.K_d or evento.key == pygame.K_RIGHT:
                self.x += 1