import pygame

class Parede():

    def __init__(self, bioma, x, y, escala) -> None:
        self.bioma = bioma
        self.x = x
        self.y = y
        self.escala = escala
        self.criarDesenhos()
    
    def criarDesenhos(self):
        x = self.x*self.escala
        y = self.y*self.escala
        self.desenhos = {
            "baubah": {"cor": (100,50,0), "pontos": ((2,2), (14,9), (19,9),(20,6), (16,3), (21,5), (28,3), (23,6), 
                                                     (23,10), (32,18), (35,16), (33,20), (33,23), (25,16), (22,24), 
                                                     (27,29), (30,28), (27,36), (21,26), (7,35), (16,25), (4,16), 
                                                     (15,19), (14,15), (10,10) )},

            "formigueiro": {"cor": (150,60,0), "pontos": ((16,8), (22,7), (27,10),(31,14), (33,20), (29,27), (24,30), (18,31), 
                                                     (11,28), (9,23), (9,18), (10,13))},

            "cacto": {"cor": (10,110,10), "pontos": ((15,14), (18,10),(23,10),(26,16),(36,16),(38,17),(37,19),(36,21),(25,22),(22,25),(17,25),(14,23),(5,23),(3,21),(3,18),(5,16))},
        }

        keys = list(self.desenhos.keys())
        for key in keys:
            self.desenhos[key]["pontos"] = tuple(map(lambda k: (k[0]+x, k[1]+y), self.desenhos[key]["pontos"]))
    
    cores = {"I": (230,230,255), "U": (30,0,40),"S": (180,150,0),"P": (100,235,100),"F": (0,50,0),"R": (150,150,150),"M": (150,0,0),"D": (255,255,0),"O": (0,0,100),"B": (255,255,0)}

    def render(self, screen):
        match self.bioma:
            case 'S':
                objeto = "baubah"
            case 'P':
                objeto = "formigueiro"
            case 'D':
                objeto = "cacto"
        pygame.draw.rect(screen, self.cores[self.bioma], pygame.Rect(self.x*self.escala, self.y*self.escala, self.escala, self.escala))
        escurecer = 0.9
        corChao = (int(self.cores[self.bioma][0]*escurecer), int(self.cores[self.bioma][1]*escurecer), int(self.cores[self.bioma][2]*escurecer))
        pygame.draw.rect(screen, corChao, pygame.Rect(self.x*self.escala, self.y*self.escala, self.escala, self.escala), border_radius=15)
        pygame.draw.polygon(screen, self.desenhos[objeto]["cor"], self.desenhos[objeto]["pontos"])