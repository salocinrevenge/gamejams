import pygame
from botao import Botao
from mundo import Mundo

class Menu():
    def __init__(self) -> None:
        self.criaBotoesMenuPrincipal()
        self.criaBotoesMenuCriar()
        self.STATE:str = "Menu"
        self.mundo = None


    def tick(self):
        if self.STATE == "Mundo":
            self.mundo.tick()

    def render(self, screen):
        if self.STATE == "Menu":
            for botao in self.botoesMenuPrincipal:
                botao.render(screen)
            return
        elif self.STATE == "Criar Sala":
            for botao in self.botoesMenuCriar:
                botao.render(screen)
            return
        elif self.STATE == "Mundo":
            self.mundo.render(screen)
            return
        
    def criarMundo(self):
        self.mundo = Mundo()

    def criaBotoesMenuPrincipal(self):
        self.botoesMenuPrincipal = []
        self.botoesMenuPrincipal.append(Botao(100, 100, 600, 150, "Criar Sala", textSize = 72))
        self.botoesMenuPrincipal.append(Botao(100, 300, 600, 150, "Carregar Sala", textSize = 72))
        self.botoesMenuPrincipal.append(Botao(100, 500, 600, 150, "Configurações", textSize = 72))

    def criaBotoesMenuCriar(self):
        self.botoesMenuCriar = []
        self.botoesMenuCriar.append(Botao(250, 650, 300, 100, "Criar", textSize = 72))

    def input(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.STATE == "Menu":
                for botao in self.botoesMenuPrincipal:
                    clique = botao.identificaClique(evento.pos)
                    if clique:
                        print(clique)
                        if clique == "Criar Sala":
                            self.STATE = clique
                            return
            if self.STATE == "Criar Sala":
                for botao in self.botoesMenuCriar:
                    clique = botao.identificaClique(evento.pos)
                    if clique:
                        print(clique)
                        if clique == "Criar":
                            self.STATE = "Mundo"
                            self.criarMundo()
                            return
        if self.STATE == "Mundo":
            self.mundo.input(evento)