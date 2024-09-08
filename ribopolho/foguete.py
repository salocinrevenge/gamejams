import pygame

class Foguete():
    def __init__(self, x, y, sala) -> None:

        self.fixedPontos = ((20,0),(28,12),(28,28),(29,30),(33,32),(35,36),(36,40),(33,36),(28,32),(22,32),(20,40),(18,32),(12,32),(7,36),(4,40),(5,36),(6,32),(8,29),(12,28),(12,12))
        self.pontos = []
        self.escala = sala.escala
        self.atualizarPosicao(x,y, sala)

    def atualizarPosicao(self, x, y, sala):
        self.sala = sala
        self.x = x
        self.y = y
        self.pontos = []
        for ponto in self.fixedPontos:
            self.pontos.append((ponto[0]+self.x*self.escala, ponto[1]+self.y*self.escala))
        
    def renderItem(self, screen,x,y,escala):
        pontosDesenho = []
        for ponto in self.fixedPontos:
            pontosDesenho.append((ponto[0]+x, ponto[1]+y))
        pygame.draw.polygon(screen, (230, 130, 0), pontosDesenho)

    def tick(self):
        pass
    
    def render(self, screen):
        # desenha o chao
        cor = self.sala.cores[self.sala.bioma]

        pygame.draw.rect(screen, cor, pygame.Rect(self.x*self.escala, self.y*self.escala, self.escala, self.escala))

        # print desenha a arvore de melancia atraves do vetor pontos
        pygame.draw.polygon(screen, (230, 130, 0), self.pontos)