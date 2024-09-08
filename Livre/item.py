import pygame

class Item():
    def __init__(self, tipo):
        self.tipo = tipo
        
    imagens = {"moeda": pygame.image.load("assets/moeda.png"), "firefox": pygame.image.load("assets/firefox.png"), 
               "pago visualCode": pygame.image.load("assets/pago visualCode.png"), "livre vscode": pygame.image.load("assets/livre vscode.png"),
               "livre libresprite": pygame.image.load("assets/livre libresprite.png")}
    
    def tick(self):
        pass
    
    def render(self, screen, pos):
        screen.blit(self.imagens[self.tipo], (pos[0], pos[1]))