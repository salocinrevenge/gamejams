import pygame
import random

class Item():
    def __init__(self, tipo):
        self.tipo = tipo
        self.tempoColido = 0
        self.velX = random.random()*2-1
        self.agiu = False
        
        
    imagens = {"moeda": pygame.image.load("assets/moeda.png"), "firefox": pygame.image.load("assets/firefox.png"), 
               "pago visualCode": pygame.image.load("assets/pago visualCode.png"), "livre vscode": pygame.image.load("assets/livre vscode.png"),
               "livre libresprite": pygame.image.load("assets/livre libresprite.png")}
    
    vida = {"moeda": 30, "firefox": 0, "pago visualCode": -30, "livre vscode": 0, "livre libresprite": 0}
    
    def tick(self):
        self.tempoColido -= 1
        
    
    def renderHUD(self, screen, pos):
        screen.blit(self.imagens[self.tipo], (pos[0], pos[1]))
        
    def render(self, screen, camera, deslocamento, pos):
        if self.tempoColido > -200:
            camera.render(screen, self.imagens[self.tipo], (pos[0]+deslocamento[0]+self.tempoColido/100+self.velX*self.tempoColido/100, pos[1]+deslocamento[1]+self.tempoColido/100))