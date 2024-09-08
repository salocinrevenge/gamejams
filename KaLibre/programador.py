import pygame
from excessoes.Win import Win
from excessoes.Die import Die

from personagem import Personagem

class Programador(Personagem):
    def __init__(self, x, y, mundo) -> None:
        super().__init__(x, y, mundo)
        self.mundo = mundo
        self.demanda = None
        self.velX = 0
        self.velY = 0
        self.vida = 100
        self.objetivos = ["livre libresprite", "livre vscode", "firefox"]
        self.acabarJogo = False
        self.contadorAcabarJogo = 200
        self.hack = None
    
    imagem = [pygame.image.load("assets/programador01.png"), pygame.image.load("assets/programador02.png"), pygame.image.load("assets/programador03.png"), pygame.image.load("assets/programador04.png")]        
    imgMoeda = pygame.image.load("assets/moeda.png")
    
    def tick(self):
        self.intervaloPassos -= 1
        if self.intervaloPassos <= 0:
            self.mover(self.velX, self.velY)
            
        if self.demanda:
            dx, dy = self.demanda
            if dy == -1:
                self.orientacao = 3
            if dy == 1:
                self.orientacao = 1
            if dx == -1:
                self.orientacao = 2
            if dx == 1:
                self.orientacao = 0
            self.mundo.salaAtual.mover(self, self.x, self.y, self.x+dx, self.y+dy)
            self.demanda = None
        for item in self.inventario:
            item.tick()
            if not item.agiu:
                item.agiu = True
                self.vidaUpdate(item.vida[item.tipo])
                if item.tipo in self.objetivos:
                    self.objetivos.remove(item.tipo)
                if len(self.objetivos) == 0:
                    self.acabarJogo = True
        if self.acabarJogo:
            self.contadorAcabarJogo -= 1
            if self.contadorAcabarJogo <= 0:
                raise Win("win")
        if self.vida <= 0:
            raise Die("lose")
        
        if self.hack == "die":
            raise Die("lose")
        if self.hack == "win":
            raise Win("win")
        super().tick()

    def vidaUpdate(self, vida):
        self.vida += vida
        if self.vida <= 0:
            self.vida = 0
        if self.vida >= 100:
            self.vida = 100
    
    
    def render(self, screen, camera, deslocamento):
        camera.render(screen, self.imagem[self.orientacao], (self.x+deslocamento[0], self.y+deslocamento[1]))
        for item in self.inventario:
            item.render(screen, camera, deslocamento, (self.x, self.y))
        super().render(screen, camera, deslocamento)
    
    def renderHUD(self, screen):
        cor = (170,170,170)
        self.renderHP(screen, cor)
        self.renderItens(screen, cor)
        

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
            if evento.key == pygame.K_SPACE:
                self.mundo.salaAtual.interagir(self)
            # if evento.key == pygame.K_0:
            #     self.vidaUpdate(-10)
            # if evento.key == pygame.K_1:
            #     self.hack = "die"
            # if evento.key == pygame.K_2:
            #     self.hack = "win"
            
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
                
                
    def renderHP(self, screen, cor):
        pygame.draw.rect(screen, cor, (10, 10, 215, 40))
        screen.blit(self.imgMoeda, (-10, 2))
        screen.blit(self.imgMoeda, ( 15, 2))
        screen.blit(self.imgMoeda, ( 40, 2))
        screen.blit(self.imgMoeda, ( 65, 2))
        screen.blit(self.imgMoeda, ( 90, 2))
        screen.blit(self.imgMoeda, (115, 2))
        screen.blit(self.imgMoeda, (140, 2))
        screen.blit(self.imgMoeda, (165, 2))
        pygame.draw.rect(screen, cor, (10+int((self.vida*215/100)), 10, int(215-(self.vida)*215/100), 40))
        
    def renderItens(self, screen, cor):
        pygame.draw.rect(screen, cor, (10, 50, 215, 40))
        i = 0
        for item in self.inventario:
            if item.tipo in ("moeda", "pago visualCode"):
                continue
            item.renderHUD(screen,(i*40,30))
            i+=1
                