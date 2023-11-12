import pygame
import random

class Parede():

    def __init__(self, bioma, x, y, escala) -> None:
        self.bioma = bioma
        self.x = x
        self.y = y
        self.escala = escala
        self.criarDesenhos()

    def clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)
    
    def clamp3(self, tupla, minn, maxn):
        return (self.clamp(tupla[0], minn, maxn), self.clamp(tupla[1], minn, maxn), self.clamp(tupla[2], minn, maxn))
    
    def criarDesenhos(self):
        x = self.x*self.escala
        y = self.y*self.escala
        var = (random.randint(0, 40)-20, random.randint(0, 40)-20, random.randint(0, 40)-20)
        self.desenhos = {
            "baubah": {"cor": self.clamp3((100+var[0],50+var[1],0+var[2]),0,255), "pontos": ((2,2), (14,9), (19,9),(20,6), (16,3), (21,5), (28,3), (23,6), (23,10), 
            (32,18), (35,16), (33,20), (33,23), (25,16), (22,24), (27,29), (30,28), (27,36), (21,26), (7,35), (16,25), (4,16), (15,19), (14,15), (10,10) )},

            "formigueiro": {"cor": self.clamp3((150+var[0],60+var[1],0+var[2]),0,255), "pontos": ((16,8), (22,7), (27,10),(31,14), (33,20), (29,27), (24,30), (18,31), 
                                                     (11,28), (9,23), (9,18), (10,13))},

            "cacto": {"cor": self.clamp3((10+var[0],110+var[1],10+var[2]),0,255), "pontos": ((15,14), (18,10),(23,10),(26,16),(36,16),(38,17),(37,19),(36,21),(25,22),
            (22,25),(17,25),(14,23),(5,23),(3,21),(3,18),(5,16))},
        
            "samauma" : {"cor": self.clamp3((60+var[0],110+var[1],60+var[2]),0,255), "pontos": ((9,7), (20,1), (35, 5), (40, 20), (35, 30), (20, 35), (10, 30), (5, 20))},

            "coqueiro" : {"cor": self.clamp3((180+var[0],200+var[1],70+var[2]),0,255), "pontos": ((20,1), (22,8), (24,12), (22, 18), (29,12), (36,8), (32,16), (22,18),
            (25, 17), (39, 20), (30, 25), (22, 22), (32,28), (38,36), (29,32), (22,22), (25, 30), (20, 39), (15, 30), (18, 20), (15, 25), (2, 20), (15, 17), (18, 18), (15, 10))},

            "rochedo" : {"cor": self.clamp3((100+var[0]//3,100+var[1]//3,100+var[2]//3),0,255), "pontos": ((9,7), (20,1), (32, 5), (37, 20), (32, 30), (20, 35), (10, 30), (5, 20))},

            "gelo" : {"cor": self.clamp3((245+(var[0]-10)//10,245+(var[1]-10)//10,255+var[2]),0,255), "pontos": ((9,7), (20,1), (35, 5), (40, 20), (35, 30), (20, 35), (10, 30), (5, 20))},

            "meteoro" : {"cor": self.clamp3((100+var[0]//3,100+var[1]//3,100+var[2]//3),0,255), "pontos": ((9,7), (20,1), (32, 5), (37, 20), (32, 30), (20, 35), (10, 30), (5, 20))},

            "marcedo" : {"cor": self.clamp3((90+var[0],10+var[1]//3,10+var[2]//3),0,255), "pontos": ((9,7), (20,1), (35, 5), (40, 20), (35, 30), (20, 35), (10, 30), (5, 20))},
        }

        keys = list(self.desenhos.keys())
        for key in keys:
            self.desenhos[key]["pontos"] = tuple(map(lambda k: (k[0]+x, k[1]+y), self.desenhos[key]["pontos"]))
    
    cores = {"I": (230,230,255), "U": (8,0,16),"S": (180,150,0),"P": (60,180,80),"F": (0,50,0),"R": (150,150,150),"M": (150,0,0),"D": (210,210,0),"O": (0,0,100),"B": (255,255,0)}

    def render(self, screen):
        escurecer = 0.9
        match self.bioma:
            case 'S':
                objeto = "baubah"
            case 'P':
                objeto = "formigueiro"
            case 'D':
                objeto = "cacto"
            case 'F':
                objeto = "samauma"
            case 'B':
                objeto = "coqueiro"
            case 'O' | 'R':
                objeto = "rochedo"
            case 'I':
                objeto = "gelo"
            case 'M':
                escurecer = 0.97
                objeto = "marcedo"
            case 'U':
                objeto = "meteoro"
            
        pygame.draw.rect(screen, self.cores[self.bioma], pygame.Rect(self.x*self.escala, self.y*self.escala, self.escala, self.escala))
        corChao = (int(self.cores[self.bioma][0]*escurecer), int(self.cores[self.bioma][1]*escurecer), int(self.cores[self.bioma][2]*escurecer))
        pygame.draw.rect(screen, corChao, pygame.Rect(self.x*self.escala, self.y*self.escala, self.escala, self.escala), border_radius=15)
        pygame.draw.polygon(screen, self.desenhos[objeto]["cor"], self.desenhos[objeto]["pontos"])