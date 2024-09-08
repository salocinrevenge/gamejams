import pygame

class Item()
    def __init__(self, tipo):
        self.tipo = tipo
        
    imagens = {"moeda": pygame.image.load("assets/moeda.png"), "firefox": pygame.image.load("assets/firefox.png")}