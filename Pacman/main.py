import pygame
import random
from pygame import mixer
import asyncio

# constantes e variaveis basicas
fps = 30
largura = 19
altura = 21
ESCALA = 35
HEIGHT = ESCALA * altura
WIDTH = ESCALA * largura
running = True
playing = True
win = False
lose = False
lives = 4
score_value = 0
debug = False
ativardebug=0
pause = True
newWalk = False

# Leste,Norte,Oeste,Sul
keys = [0, 0, 0, 0]

pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman")
icon = pygame.image.load("pacIcon.png")
pygame.display.set_icon(icon)

# Background Sound
mixer.music.load("pacman.mp3")
sound = True
if sound:
    print("tocando")
    mixer.music.play(-1)


# funçoes basicas
def clamp(num1, min, max):
    if num1 > max:
        return max
    elif num1 < min:
        return min
    else:
        return num1


def modclamp(num1, min, max):
    if abs(num1) > max:
        return max * (num1 / abs(num1))
    elif abs(num1) < min:
        return min * (num1 // abs(num1))
    else:
        return num1


def entre(num1, min, max):
    if max >= num1 >= min:
        return True
    else:
        return False


def dentroRect(x1, y1, x2, y2, tam):
    if entre(x1, min(x2, x2 + tam), max(x2, x2 + tam)) and entre(y1, min(y2, y2 + tam), max(y2, y2 + tam)):
        return True
    else:
        return False

def dentroRect2(x1, y1, x2, x3, y2, y3):
    if entre(x1, min(x2, x3), max(x2, x3)) and entre(y1, min(y2, y3), max(y2, y3)):
        return True
    else:
        return False

def colideRect(objeto1, tamanho1, objeto2, tamanho2):
    if dentroRect(objeto1.x, objeto1.y, objeto2.x, objeto2.y, tamanho2) or dentroRect(objeto1.x + tamanho1, objeto1.y,
                                                                                      objeto2.x, objeto2.y,
                                                                                      tamanho2) or dentroRect(
            objeto1.x + tamanho1, objeto1.y + tamanho1, objeto2.x, objeto2.y, tamanho2) or dentroRect(objeto1.x,
                                                                                                      objeto1.y + tamanho1,
                                                                                                      objeto2.x,
                                                                                                      objeto2.y,
                                                                                                      tamanho2):
        return True

    else:
        return False

def naGrade(x1,y1,tamanho):
    if x1//ESCALA == (x1+tamanho)//ESCALA and y1//ESCALA == (y1+tamanho)//ESCALA:
        return True
    else:
        return False

# mostrar hud
def show_hud(x, y):
    global lives
    vidas = pygame.image.load("vidas.png")
    score = font.render("Score: " + str(score_value) + "  Vidas: ", True, (100, 255, 255))
    screen.blit(score, (x, y))
    for i in range(lives - 1):
        screen.blit(vidas, (x + 300 + (i * ESCALA), y))

class Rect:

    def __init__(self,x1,x2,y1,y2,red,green,blue):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.skin = pygame.Surface((abs(x2-x1), abs(y2-y1))).convert()
        self.skin.fill((red,green,blue))
        self.skin.set_alpha(100)

    def display(self):
        screen.blit(self.skin,(self.x1,self.y1))


# mapa
class Mapa:
    wallSkin = pygame.Surface((ESCALA, ESCALA))
    wallSkin.fill((0, 30, 200))
    gateSkin = pygame.Surface((ESCALA, ESCALA))
    gateSkin.fill((0, 10, 200 // 3))
    foodSkin = pygame.image.load("food.png")

    def __init__(self, mapa, nlinhas, ncolunas):
        self.mapa = mapa
        self.nlinhas = nlinhas
        self.ncolunas = ncolunas

    def write(self):
        for i in range(self.nlinhas):
            for j in range(self.ncolunas):
                if self.mapa[i][j] !=  "\n":
                    print(self.mapa[i][j] + " ", end="")
            print("")

    def inicializarObjetos(self, jogador, fantasmaAzul, fantasmaVermelho, fantasmaLaranga, fantasmaVerde):
        for i in range(self.nlinhas):
            for j in range(self.ncolunas):
                if self.mapa[i][j] == "P":
                    jogador.x = (j * ESCALA)
                    jogador.y = (i * ESCALA)
                if self.mapa[i][j] == "B":
                    fantasmaAzul.x = (j * ESCALA)
                    fantasmaAzul.y = (i * ESCALA)
                    fantasmaVerde.x = (j * ESCALA)
                    fantasmaVerde.y = (i * ESCALA)
                if self.mapa[i][j] == "R":
                    fantasmaVermelho.x = (j * ESCALA)
                    fantasmaVermelho.y = (i * ESCALA)
                if self.mapa[i][j] == "O":
                    fantasmaLaranga.x = (j * ESCALA)
                    fantasmaLaranga.y = (i * ESCALA)

    def display(self):
        for i in range(self.nlinhas):
            for j in range(self.ncolunas):
                if self.mapa[i][j] == "#":
                    screen.blit(self.wallSkin, (j * ESCALA, i * ESCALA))
                elif self.mapa[i][j] == ".":
                    screen.blit(self.foodSkin, (j * ESCALA, i * ESCALA))
                elif self.mapa[i][j] == "@":
                    screen.blit(self.gateSkin, (j * ESCALA, i * ESCALA))

    def colisionRectMap(self, x1, y1, tamanho, id):
        if self.mapa[y1 // ESCALA][x1 // ESCALA] == "#" or (
                self.mapa[y1 // ESCALA][x1 // ESCALA] == "@" and id == "Pac") or \
                self.mapa[(y1 + tamanho - 1) // ESCALA][x1 // ESCALA] == "#" or (
                self.mapa[(y1 + tamanho - 1) // ESCALA][
                    x1 // ESCALA] == "@" and id == "Pac") or self.mapa[y1 // ESCALA][
            (x1 + tamanho - 1) // ESCALA] == "#" or \
                (self.mapa[y1 // ESCALA][(x1 + tamanho - 1) // ESCALA] == "@" and id == "Pac") or \
                self.mapa[(y1 + tamanho - 1) // ESCALA][
                    (x1 + tamanho - 1) // ESCALA] == "#" or (self.mapa[(y1 + tamanho - 1) // ESCALA][
                                                                 (
                                                                         x1 + tamanho - 1) // ESCALA] == "@" and id == "Pac") or (
                self.mapa[y1 // ESCALA][x1 // ESCALA] == "/" and id == "Ghost") or (
                self.mapa[(y1 + tamanho - 1) // ESCALA][x1 // ESCALA] == "/" and id == "Ghost") or (
                self.mapa[y1 // ESCALA][(x1 + tamanho - 1) // ESCALA] == "/" and id == "Ghost") or (
                self.mapa[(y1 + tamanho - 1) // ESCALA][(x1 + tamanho - 1) // ESCALA] == "/" and id == "Ghost"):
            return True
        else:
            return False

    def colisionRectFood(self, x1, y1, tamanho):
        global score_value
        if self.mapa[y1 // ESCALA][x1 // ESCALA] == ".":
            self.mapa[y1 // ESCALA][x1 // ESCALA] = " "
            score_value += 1
            if sound:
                food_sound.play()
        elif self.mapa[(y1 + tamanho - 1) // ESCALA][x1 // ESCALA] == ".":
            self.mapa[(y1 + tamanho - 1) // ESCALA][x1 // ESCALA] = " "
            score_value += 1
            if sound:
                food_sound.play()
        elif self.mapa[y1 // ESCALA][(x1 + tamanho - 1) // ESCALA] == ".":
            self.mapa[y1 // ESCALA][(x1 + tamanho - 1) // ESCALA] = " "
            score_value += 1
            if sound:
                food_sound.play()
        elif self.mapa[(y1 + tamanho - 1) // ESCALA][(x1 + tamanho - 1) // ESCALA] == ".":
            self.mapa[(y1 + tamanho - 1) // ESCALA][(x1 + tamanho - 1) // ESCALA] = " "
            score_value += 1
            if sound:
                food_sound.play()


# pacman
class Pacman:
    ivuneravelTime = 0
    sensores = pygame.Surface((ESCALA, ESCALA))
    pacmanL = pygame.image.load("pacman L.png").convert()
    pacmanN = pygame.image.load("pacman N.png").convert()
    pacmanO = pygame.image.load("pacman O.png").convert()
    pacmanS = pygame.image.load("pacman S.png").convert()
    pacmanNO = pygame.image.load("pacman NO.png").convert()
    pacmanNE = pygame.image.load("pacman NE.png").convert()
    pacmanSO = pygame.image.load("pacman SO.png").convert()
    pacmanSE = pygame.image.load("pacman SE.png").convert()

    pacmanN.set_colorkey((0, 0, 0))
    pacmanO.set_colorkey((0, 0, 0))
    pacmanS.set_colorkey((0, 0, 0))
    pacmanNO.set_colorkey((0, 0, 0))
    pacmanNE.set_colorkey((0, 0, 0))
    pacmanSO.set_colorkey((0, 0, 0))
    pacmanSE.set_colorkey((0, 0, 0))

    # caminhos abertos (Leste,Norte,Oeste,Sul)
    validos = [False, False, False, False]
    request= "null"
    nvalidos = 0
    acelleration = 5
    velX = 0
    velY = 0
    x: int
    y: int

    def encontrarCaminhosValidos(self, mapa):
        total = 0
        if self.x+(ESCALA*2)>WIDTH:
            pass
        elif not mapa.colisionRectMap(self.x + ESCALA, self.y, ESCALA, "Pac"):
            self.validos[0] = True
            total += 1
        else:
            self.validos[0] = False
        if not mapa.colisionRectMap(self.x, self.y - ESCALA, ESCALA, "Pac"):
            self.validos[1] = True
            total += 1
        else:
            self.validos[1] = False
        if self.x-self.acelleration <= self.acelleration:
            pass
        elif not mapa.colisionRectMap(self.x - ESCALA, self.y, ESCALA, "Pac"):
            self.validos[2] = True
            total += 1
        else:
            self.validos[2] = False
        if not mapa.colisionRectMap(self.x, self.y + ESCALA, ESCALA, "Pac"):
            self.validos[3] = True
            total += 1
        else:
            self.validos[3] = False
        self.nvalidos = total

    def displaySensores(self, mapa):
        # ta verde ou ta maduro?
        if self.x-self.acelleration <=self.acelleration:
            pass
        elif mapa.colisionRectMap(self.x - ESCALA, self.y, ESCALA, "Pac"):
            self.sensores.fill((255, 0, 0))
        else:
            self.sensores.fill((0, 255, 0))
        if debug:
            screen.blit(self.sensores, (self.x - ESCALA, self.y))
        if self.x + (ESCALA*2) >= WIDTH:
            pass
        elif mapa.colisionRectMap(self.x + ESCALA, self.y, ESCALA, "Pac"):
            self.sensores.fill((255, 0, 0))
        else:
            self.sensores.fill((0, 255, 0))
        if debug:
            screen.blit(self.sensores, (self.x + ESCALA, self.y))
        if mapa.colisionRectMap(self.x, self.y - ESCALA, ESCALA, "Pac"):
            self.sensores.fill((255, 0, 0))
        else:
            self.sensores.fill((0, 255, 0))
        if debug:
            screen.blit(self.sensores, (self.x, self.y - ESCALA))
        if mapa.colisionRectMap(self.x, self.y + ESCALA, ESCALA, "Pac"):
            self.sensores.fill((255, 0, 0))
        else:
            self.sensores.fill((0, 255, 0))
        if debug:
            screen.blit(self.sensores, (self.x, self.y + ESCALA))
        self.encontrarCaminhosValidos(self, mapa)

    def display(self):

        intervalopiscando = 15
        if self.ivuneravelTime > 0:
            self.pacmanL.set_alpha(clamp(255 - self.ivuneravelTime, 50, 255))
            self.pacmanN.set_alpha(clamp(255 - self.ivuneravelTime, 50, 255))
            self.pacmanO.set_alpha(clamp(255 - self.ivuneravelTime, 50, 255))
            self.pacmanS.set_alpha(clamp(255 - self.ivuneravelTime, 50, 255))
            self.pacmanNO.set_alpha(clamp(255 - self.ivuneravelTime, 50, 255))
            self.pacmanNE.set_alpha(clamp(255 - self.ivuneravelTime, 50, 255))
            self.pacmanSO.set_alpha(clamp(255 - self.ivuneravelTime, 50, 255))
            self.pacmanSE.set_alpha(clamp(255 - self.ivuneravelTime, 50, 255))
        if not ((self.ivuneravelTime + intervalopiscando) // intervalopiscando) % 3 == 0:
            if self.velX > 0 and self.velY == 0:
                screen.blit(self.pacmanL, (self.x, self.y))
            elif self.velX > 0 and self.velY > 0:
                screen.blit(self.pacmanSE, (self.x, self.y))
            elif self.velX > 0 and self.velY < 0:
                screen.blit(self.pacmanNE, (self.x, self.y))
            elif self.velX == 0 and self.velY == 0:
                screen.blit(self.pacmanL, (self.x, self.y))
            elif self.velX == 0 and self.velY < 0:
                screen.blit(self.pacmanN, (self.x, self.y))
            elif self.velX == 0 and self.velY > 0:
                screen.blit(self.pacmanS, (self.x, self.y))
            elif self.velX < 0 and self.velY == 0:
                screen.blit(self.pacmanO, (self.x, self.y))
            elif self.velX < 0 and self.velY > 0:
                screen.blit(self.pacmanSO, (self.x, self.y))
            elif self.velX < 0 and self.velY < 0:
                screen.blit(self.pacmanNO, (self.x, self.y))

    def tick(self, mapa):
        # Portal 2
        if (self.x + ESCALA) > (WIDTH - self.acelleration):
            self.x = 0
        if self.x < 0:
            self.x = WIDTH - ESCALA

        if not newWalk and self.validos[0] and self.request == "leste":
            self.velY=0
            self.velX= self.acelleration
        elif not newWalk and self.validos[1] and self.request == "norte":
            self.velY= -self.acelleration
            self.velX= 0
        elif not newWalk and self.validos[2] and self.request == "oeste":
            self.velY=0
            self.velX= -self.acelleration
        elif not newWalk and self.validos[3] and self.request == "sul":
            self.velY= self.acelleration
            self.velX= 0

        # Tu não vais bater na parede não!
        if not mapa.colisionRectMap(self.x + self.velX, self.y, ESCALA, "Pac"):
            self.x += self.velX
        if debug:
            print("X: "+ str(self.x), end="")
        if not mapa.colisionRectMap(self.x, self.y + self.velY, ESCALA, "Pac"):
            self.y += self.velY
        if debug:
            print(" Y: " + str(self.y))

        # bateu uma fome, vou comer
        mapa.colisionRectFood(self.x, self.y, ESCALA)

        # Eu sou inevitavel!
        if self.ivuneravelTime > 0:
            self.ivuneravelTime -= 5


# fantasma aleatório
class BlueGhost:
    sensores = pygame.Surface((ESCALA, ESCALA))
    blueghost = pygame.image.load("Bghost S.png")
    acceleration = 5
    x: int
    y: int
    velX = 0
    velY = 0
    # caminhos abertos (Leste,Norte,Oeste,Sul)
    validos = [False, False, False, False]
    nvalidos = 0

    def __init__(self, mapa):
        self.mapa = mapa

    def display(self):
        screen.blit(self.blueghost, (self.x, self.y))

    def displaySensores(self, mapa):
        # ta verde ou ta maduro?
        if mapa.colisionRectMap(self.x - ESCALA, self.y, ESCALA, "Ghost"):
            self.sensores.fill((255, 0, 0))
        else:
            self.sensores.fill((0, 255, 0))
        if debug:
            screen.blit(self.sensores, (self.x - ESCALA, self.y))
        if mapa.colisionRectMap(self.x + ESCALA, self.y, ESCALA, "Ghost"):
            self.sensores.fill((255, 0, 0))
        else:
            self.sensores.fill((0, 255, 0))
        if debug:
            screen.blit(self.sensores, (self.x + ESCALA, self.y))
        if mapa.colisionRectMap(self.x, self.y - ESCALA, ESCALA, "Ghost"):
            self.sensores.fill((255, 0, 0))
        else:
            self.sensores.fill((0, 255, 0))
        if debug:
            screen.blit(self.sensores, (self.x, self.y - ESCALA))
        if mapa.colisionRectMap(self.x, self.y + ESCALA, ESCALA, "Ghost"):
            self.sensores.fill((255, 0, 0))
        else:
            self.sensores.fill((0, 255, 0))
        if debug:
            screen.blit(self.sensores, (self.x, self.y + ESCALA))
        self.encontrarCaminhosValidos(mapa)

    def writeValidos(self):
        for i in range(4):
            print("validos na posicao " + str(i) + " vale " + str(self.validos[i]))

    def encontrarCaminhosValidos(self, mapa):
        total = 0
        if not mapa.colisionRectMap(self.x + ESCALA, self.y, ESCALA, "Ghost"):
            self.validos[0] = True
            total += 1
        else:
            self.validos[0] = False
        if not mapa.colisionRectMap(self.x, self.y - ESCALA, ESCALA, "Ghost"):
            self.validos[1] = True
            total += 1
        else:
            self.validos[1] = False
        if not mapa.colisionRectMap(self.x - ESCALA, self.y, ESCALA, "Ghost"):
            self.validos[2] = True
            total += 1
        else:
            self.validos[2] = False
        if not mapa.colisionRectMap(self.x, self.y + ESCALA, ESCALA, "Ghost"):
            self.validos[3] = True
            total += 1
        else:
            self.validos[3] = False
        self.nvalidos = total

    def inteligencia(self, mapa):
        if self.mapa[self.y // ESCALA][self.x // ESCALA] == "B":
            self.velY = -self.acceleration
        elif self.mapa[self.y // ESCALA][self.x // ESCALA] == "." or self.mapa[self.y // ESCALA][
            self.x // ESCALA] == "P" or self.mapa[self.y // ESCALA][self.x // ESCALA] == " ":
            if (self.nvalidos > 2 or mapa.colisionRectMap(self.x + self.velX, self.y + self.velY, ESCALA,
                                                          "Ghost")) and self.nvalidos > 0:
                self.velX = 0
                self.velY = 0
                while True:
                    rand = random.randint(0, 3)
                    if rand == 0 and self.validos[0]:
                        self.velX = self.acceleration
                        break
                    elif rand == 1 and self.validos[1]:
                        self.velY = -self.acceleration
                        break
                    elif rand == 2 and self.validos[2]:
                        self.velX = -self.acceleration
                        break
                    elif rand == 3 and self.validos[3] and not mapa.colisionRectMap(self.x, self.y + ESCALA, ESCALA,
                                                                                    "Pac"):
                        self.velY = self.acceleration
                        break

    def tick(self, mapa):
        self.inteligencia(mapa)
        if not mapa.colisionRectMap(self.x + self.velX, self.y, ESCALA, "Ghost"):
            self.x += self.velX
        if not mapa.colisionRectMap(self.x, self.y + self.velY, ESCALA, "Ghost"):
            self.y += self.velY

# fantasma que segue
class RedGhost:
    wallSkin = pygame.Surface((ESCALA, ESCALA))
    wallSkin.fill((0, 30, 200))
    pacSkin = pygame.Surface((ESCALA, ESCALA))
    pacSkin.fill((255, 0, 10))
    mapa2 = []
    setaOeste = pygame.image.load("setaOesteR.png")
    setaLeste = pygame.image.load("setaLesteR.png")
    setaNorte = pygame.image.load("setaNorteR.png")
    setaSul = pygame.image.load("setaSulR.png")
    redghostImage = pygame.image.load("Rghost S.png")
    acceleration = 4
    x: int
    y: int
    velX = -acceleration
    velY = 0

    def __init__(self, mapa, nlinhas, ncolunas):
        self.nlinhas = nlinhas
        self.ncolunas = ncolunas
        # criar um mapa independente do original
        for i in range(self.nlinhas):
            linha2 = []
            for j in range(self.ncolunas):
                if mapa[i][j] !=  "P":
                    linha2.append(mapa[i][j])
                else:
                    linha2.append(".")
            self.mapa2.append(linha2)

    def write(self):
        for i in range(self.nlinhas):
            for j in range(self.ncolunas):
                if self.mapa2[i][j] !=  "\n":
                    print(self.mapa2[i][j] + " ", end="")

    def limparCaminhos(self):
        for i in range(self.nlinhas):
            for j in range(self.ncolunas):
                if self.mapa2[i][j] == "<" or self.mapa2[i][j] == ">" or self.mapa2[i][j] == "A" or self.mapa2[i][j] == "V" or self.mapa2[i][j] == "R" or self.mapa2[i][j] == "P" or self.mapa2[i][j] == "B":
                    self.mapa2[i][j] = "."

    def criarMapaCaminhos(self, pacman):
        self.limparCaminhos()
        if dentroRect2(pacman.x, pacman.y, -10,135,310,320) or dentroRect2(pacman.x,pacman.y,515,640,310,320):
            novos = [(315 // ESCALA, 525 // ESCALA)]

        else:
            novos = [((pacman.y // ESCALA), (pacman.x // ESCALA))]
        self.mapa2[novos[0][0]][novos[0][1]] = "P"
        self.mapa2[self.y//ESCALA][self.x//ESCALA] = "R"
        processando = True
        tmp = 1
        while processando:
            nnovos = tmp
            tmp = 0
            for i in range(nnovos):
                if novos[0][0] ==(self.y//ESCALA) and novos[0][1] == (self.x//ESCALA):
                    processando = False
                    break
                if self.mapa2[novos[0][0]+1][novos[0][1]] == "." or self.mapa2[novos[0][0]+1][novos[0][1]] == " " or self.mapa2[novos[0][0]+1][novos[0][1]] == "@" or self.mapa2[novos[0][0]+1][novos[0][1]] == "R":
                    self.mapa2[novos[0][0]+1][novos[0][1]] = "A"
                    tmp += 1
                    novos.append((novos[0][0]+1, novos[0][1]))
                if self.mapa2[novos[0][0]][novos[0][1]-1] == "." or self.mapa2[novos[0][0]][novos[0][1]-1] == " " or self.mapa2[novos[0][0]][novos[0][1]-1] == "@" or self.mapa2[novos[0][0]][novos[0][1]-1] == "R":
                    self.mapa2[novos[0][0]][novos[0][1]-1] = ">"
                    tmp += 1
                    novos.append((novos[0][0], novos[0][1]-1))
                if self.mapa2[novos[0][0]-1][novos[0][1]] == "." or self.mapa2[novos[0][0]-1][novos[0][1]] == " " or self.mapa2[novos[0][0]-1][novos[0][1]] == "@" or self.mapa2[novos[0][0]-1][novos[0][1]] == "R":
                    self.mapa2[novos[0][0]-1][novos[0][1]] = "V"
                    tmp += 1
                    novos.append((novos[0][0]-1, novos[0][1]))
                if self.mapa2[novos[0][0]][novos[0][1] + 1] == "." or self.mapa2[novos[0][0]][novos[0][1] + 1] == " " or self.mapa2[novos[0][0]][novos[0][1] + 1] == "@" or self.mapa2[novos[0][0]][novos[0][1] + 1] == "R":
                    self.mapa2[novos[0][0]][novos[0][1] + 1] = "<"
                    tmp += 1
                    novos.append((novos[0][0], novos[0][1] + 1))
                novos.pop(0)

    def seguirCaminho(self):
        if self.mapa2[self.y//ESCALA][self.x//ESCALA] == "<" and naGrade(self.x, self.y,ESCALA-self.acceleration):
            self.velX = -self.acceleration
            self.velY = 0
        elif self.mapa2[self.y//ESCALA][self.x//ESCALA] == ">" and naGrade(self.x, self.y,ESCALA-self.acceleration):
            self.velX = +self.acceleration
            self.velY = 0
        elif self.mapa2[self.y//ESCALA][self.x//ESCALA] == "A" and naGrade(self.x, self.y,ESCALA-self.acceleration):
            self.velY = -self.acceleration
            self.velX = 0
        elif self.mapa2[self.y//ESCALA][self.x//ESCALA] == "V" and naGrade(self.x, self.y,ESCALA-self.acceleration):
            self.velY = +self.acceleration
            self.velX = 0
        else:
            pass

    def inteligencia(self, pacman):
        self.criarMapaCaminhos(pacman)
        self.seguirCaminho()
        pass

    def tick(self, pacman, mapa):
        self.inteligencia(pacman)
        if not mapa.colisionRectMap(self.x + self.velX, self.y, ESCALA-self.acceleration+1, "Ghost"):
            self.x += self.velX
        if not mapa.colisionRectMap(self.x, self.y + self.velY, ESCALA-self.acceleration+1, "Ghost"):
            self.y += self.velY

    def display(self):
        screen.blit(self.redghostImage, (self.x, self.y))

    def displayMapa(self):
        for i in range(self.nlinhas):
            for j in range(self.ncolunas):
                if self.mapa2[i][j] == "#":
                    screen.blit(self.wallSkin, (j * ESCALA, i * ESCALA))
                elif self.mapa2[i][j] == "P":
                    screen.blit(self.pacSkin, (j * ESCALA, i * ESCALA))
                elif self.mapa2[i][j] == "<":
                    screen.blit(self.setaOeste, (j * ESCALA, i * ESCALA))
                elif self.mapa2[i][j] == ">":
                    screen.blit(self.setaLeste, (j * ESCALA, i * ESCALA))
                elif self.mapa2[i][j] == "A":
                    screen.blit(self.setaNorte, (j * ESCALA, i * ESCALA))
                elif self.mapa2[i][j] == "V":
                    screen.blit(self.setaSul, (j * ESCALA, i * ESCALA))

class OrangeGhost:
    wallSkin = pygame.Surface((ESCALA, ESCALA))
    wallSkin.fill((0, 30, 200))
    pacSkin = pygame.Surface((ESCALA, ESCALA))
    pacSkin.fill((255, 100, 10))
    mapa2 = []
    setaOeste = pygame.image.load("setaOesteO.png")
    setaLeste = pygame.image.load("setaLesteO.png")
    setaNorte = pygame.image.load("setaNorteO.png")
    setaSul = pygame.image.load("setaSulO.png")
    image = pygame.image.load("Oghost S.png")
    acceleration = 3
    x: int
    y: int
    velX = -acceleration
    velY = 0
    retangulos = []
    retangulos.append(Rect(35,140+ESCALA,35,175+ESCALA,255,150,200))
    retangulos.append(Rect(490-1, 595 + ESCALA, 35, 175 + ESCALA, 255,150,200))
    retangulos.append(Rect(35,140+ESCALA,455,595+ESCALA,255,150,200))
    retangulos.append(Rect(490-1, 595 + ESCALA, 455, 595 + ESCALA, 255,150,200))
    retangulos.append(Rect(140+ESCALA, 420-1 + ESCALA+ESCALA, 525, 665 + ESCALA, 150, 150, 255))
    retangulos.append(Rect(140 + ESCALA, 420-1 + ESCALA+ESCALA, 35, 105 + ESCALA, 150, 150, 255))
    retangulos.append(Rect(210 - ESCALA, 490-1, 175-ESCALA, 525, 150, 255, 150))
    retangulos.append(Rect(35, 140+ESCALA, 665 - ESCALA, 665+ESCALA, 255, 255, 150))
    retangulos.append(Rect(490-1, 595 + ESCALA, 665 - ESCALA, 665 + ESCALA, 255, 255, 150))
    retangulos.append(Rect(140, 140 + ESCALA, 175 + ESCALA, 455, 255, 255, 150))
    retangulos.append(Rect(490-1, 490 + ESCALA, 175 + ESCALA, 455, 255, 255, 150))

    def __init__(self, mapa, nlinhas, ncolunas):
        self.nlinhas = nlinhas
        self.ncolunas = ncolunas
        # criar um mapa independente do original
        for i in range(self.nlinhas):
            linha2 = []
            for j in range(self.ncolunas):
                if mapa[i][j] !=  "P":
                    linha2.append(mapa[i][j])
                else:
                    linha2.append(".")
            self.mapa2.append(linha2)

    def write(self):
        for i in range(self.nlinhas):
            for j in range(self.ncolunas):
                if self.mapa2[i][j] !=  "\n":
                    print(self.mapa2[i][j] + " ", end="")

    def limparCaminhos(self):
        for i in range(self.nlinhas):
            for j in range(self.ncolunas):
                if self.mapa2[i][j] == "<" or self.mapa2[i][j] == ">" or self.mapa2[i][j] == "A" or self.mapa2[i][j] == "V" or self.mapa2[i][j] == "R" or self.mapa2[i][j] == "P" or self.mapa2[i][j] == "B":
                    self.mapa2[i][j] = "."

    def criarMapaCaminhos(self, x,y):
        self.limparCaminhos()
        if dentroRect2(x, y, -10,135,310,320) or dentroRect2(x,y,515,640,310,320):
            novos = [(315 // ESCALA, (140-ESCALA) // ESCALA)]

        else:
            novos = [((y // ESCALA), (x // ESCALA))]
        self.mapa2[novos[0][0]][novos[0][1]] = "P"
        self.mapa2[self.y//ESCALA][self.x//ESCALA] = "R"
        processando = True
        tmp = 1
        while processando:
            nnovos = tmp
            tmp = 0
            for i in range(nnovos):
                if novos[0][0] ==(self.y//ESCALA) and novos[0][1] == (self.x//ESCALA):
                    processando = False
                    break
                if self.mapa2[novos[0][0]+1][novos[0][1]] == "." or self.mapa2[novos[0][0]+1][novos[0][1]] == " " or self.mapa2[novos[0][0]+1][novos[0][1]] == "@" or self.mapa2[novos[0][0]+1][novos[0][1]] == "R":
                    self.mapa2[novos[0][0]+1][novos[0][1]] = "A"
                    tmp += 1
                    novos.append((novos[0][0]+1, novos[0][1]))
                if self.mapa2[novos[0][0]][novos[0][1]-1] == "." or self.mapa2[novos[0][0]][novos[0][1]-1] == " " or self.mapa2[novos[0][0]][novos[0][1]-1] == "@" or self.mapa2[novos[0][0]][novos[0][1]-1] == "R":
                    self.mapa2[novos[0][0]][novos[0][1]-1] = ">"
                    tmp += 1
                    novos.append((novos[0][0], novos[0][1]-1))
                if self.mapa2[novos[0][0]-1][novos[0][1]] == "." or self.mapa2[novos[0][0]-1][novos[0][1]] == " " or self.mapa2[novos[0][0]-1][novos[0][1]] == "@" or self.mapa2[novos[0][0]-1][novos[0][1]] == "R":
                    self.mapa2[novos[0][0]-1][novos[0][1]] = "V"
                    tmp += 1
                    novos.append((novos[0][0]-1, novos[0][1]))
                if self.mapa2[novos[0][0]][novos[0][1] + 1] == "." or self.mapa2[novos[0][0]][novos[0][1] + 1] == " " or self.mapa2[novos[0][0]][novos[0][1] + 1] == "@" or self.mapa2[novos[0][0]][novos[0][1] + 1] == "R":
                    self.mapa2[novos[0][0]][novos[0][1] + 1] = "<"
                    tmp += 1
                    novos.append((novos[0][0], novos[0][1] + 1))
                novos.pop(0)

    def seguirCaminho(self):
        if self.mapa2[self.y//ESCALA][self.x//ESCALA] == "P" and naGrade(self.x, self.y,ESCALA-self.acceleration):
            self.velY = 0
            self.velX = 0
        elif self.mapa2[self.y//ESCALA][self.x//ESCALA] == "<" and naGrade(self.x, self.y,ESCALA-self.acceleration):
            self.velX = -self.acceleration
            self.velY = 0
        elif self.mapa2[self.y//ESCALA][self.x//ESCALA] == ">" and naGrade(self.x, self.y,ESCALA-self.acceleration):
            self.velX = +self.acceleration
            self.velY = 0
        elif self.mapa2[self.y//ESCALA][self.x//ESCALA] == "A" and naGrade(self.x, self.y,ESCALA-self.acceleration):
            self.velY = -self.acceleration
            self.velX = 0
        elif self.mapa2[self.y//ESCALA][self.x//ESCALA] == "V" and naGrade(self.x, self.y,ESCALA-self.acceleration):

            self.velY = +self.acceleration
            self.velX = 0


    def inteligencia(self, pacman):
        if dentroRect2(pacman.x, pacman.y, self.retangulos[0].x1, self.retangulos[0].x2, self.retangulos[0].y1, self.retangulos[0].y2):
            self.criarMapaCaminhos(140, pacman.y)
        elif dentroRect2(pacman.x, pacman.y, self.retangulos[1].x1, self.retangulos[1].x2, self.retangulos[1].y1, self.retangulos[1].y2):
            self.criarMapaCaminhos(490, pacman.y)
        elif dentroRect2(pacman.x, pacman.y+1, self.retangulos[2].x1, self.retangulos[2].x2, self.retangulos[2].y1, self.retangulos[2].y2):
            self.criarMapaCaminhos(140, pacman.y)
        elif dentroRect2(pacman.x, pacman.y+1, self.retangulos[3].x1, self.retangulos[3].x2, self.retangulos[3].y1, self.retangulos[3].y2):
            self.criarMapaCaminhos(490, pacman.y)
        elif dentroRect2(pacman.x, pacman.y+1, self.retangulos[4].x1, self.retangulos[4].x2, self.retangulos[4].y1, self.retangulos[4].y2):
            self.criarMapaCaminhos(pacman.x, 525)
        elif dentroRect2(pacman.x, pacman.y+1, self.retangulos[5].x1, self.retangulos[5].x2, self.retangulos[5].y1, self.retangulos[5].y2):
            self.criarMapaCaminhos(pacman.x, 105)
        elif dentroRect2(pacman.x, pacman.y+1, self.retangulos[6].x1, self.retangulos[6].x2, self.retangulos[6].y1, self.retangulos[6].y2):
            if player.x <= 330:
                self.criarMapaCaminhos(140, pacman.y)
            else:
                self.criarMapaCaminhos(490, pacman.y)
        elif dentroRect2(pacman.x, pacman.y+1, self.retangulos[7].x1, self.retangulos[7].x2, self.retangulos[7].y1, self.retangulos[7].y2):
            if player.velX<0:
                self.criarMapaCaminhos(35, 595)
            elif player.velX>0:
                self.criarMapaCaminhos(210-ESCALA, 665)
        elif dentroRect2(pacman.x, pacman.y+1, self.retangulos[8].x1, self.retangulos[8].x2, self.retangulos[8].y1, self.retangulos[8].y2):
            if player.velX>0:
                self.criarMapaCaminhos(595, 595)
            elif player.velX<0:
                self.criarMapaCaminhos(490-ESCALA, 665)
        elif dentroRect2(pacman.x, pacman.y+1, self.retangulos[9].x1, self.retangulos[9].x2, self.retangulos[9].y1, self.retangulos[9].y2) or dentroRect2(pacman.x, pacman.y+1, self.retangulos[10].x1, self.retangulos[10].x2, self.retangulos[10].y1, self.retangulos[10].y2):
            if player.velY < 0:
                self.criarMapaCaminhos(pacman.x, 175)
            if player.velY > 0:
                self.criarMapaCaminhos(pacman.x, 455)
        else:
            self.criarMapaCaminhos(pacman.x, pacman.y)
        self.seguirCaminho()
        pass

    def tick(self, pacman, mapa):
        self.inteligencia(pacman)
        if not mapa.colisionRectMap(self.x + self.velX, self.y, ESCALA-self.acceleration+1, "Ghost"):
            self.x += self.velX
        if not mapa.colisionRectMap(self.x, self.y + self.velY, ESCALA-self.acceleration+1, "Ghost"):
            self.y += self.velY

    def display(self):
        screen.blit(self.image, (self.x, self.y))
        if debug:
            for rec in self.retangulos:
                rec.display()

    def displayMapa(self):
        for i in range(self.nlinhas):
            for j in range(self.ncolunas):
                if self.mapa2[i][j] == "#":
                    screen.blit(self.wallSkin, (j * ESCALA, i * ESCALA))
                elif self.mapa2[i][j] == "P":
                    screen.blit(self.pacSkin, (j * ESCALA, i * ESCALA))
                elif self.mapa2[i][j] == "<":
                    screen.blit(self.setaOeste, (j * ESCALA, i * ESCALA))
                elif self.mapa2[i][j] == ">":
                    screen.blit(self.setaLeste, (j * ESCALA, i * ESCALA))
                elif self.mapa2[i][j] == "A":
                    screen.blit(self.setaNorte, (j * ESCALA, i * ESCALA))
                elif self.mapa2[i][j] == "V":
                    screen.blit(self.setaSul, (j * ESCALA, i * ESCALA))

class GreenGhost:
    wallSkin = pygame.Surface((ESCALA, ESCALA))
    wallSkin.fill((0, 30, 200))
    pacSkin = pygame.Surface((ESCALA, ESCALA))
    pacSkin.fill((0, 255, 10))
    mapa2 = []
    setaOeste = pygame.image.load("setaOeste.png")
    setaLeste = pygame.image.load("setaLeste.png")
    setaNorte = pygame.image.load("setaNorte.png")
    setaSul = pygame.image.load("setaSul.png")
    image = pygame.image.load("Gghost S.png")
    acceleration = 4
    x: int
    y: int
    velX = 0
    velY = 0

    def __init__(self, mapa, nlinhas, ncolunas):
        self.nlinhas = nlinhas
        self.ncolunas = ncolunas
        # criar um mapa independente do original
        for i in range(self.nlinhas):
            linha2 = []
            for j in range(self.ncolunas):
                if mapa[i][j] !=  "P":
                    linha2.append(mapa[i][j])
                else:
                    linha2.append(".")
            self.mapa2.append(linha2)

    def write(self):
        for i in range(self.nlinhas):
            for j in range(self.ncolunas):
                if self.mapa2[i][j] !=  "\n":
                    print(self.mapa2[i][j] + " ", end="")

    def limparCaminhos(self):
        for i in range(self.nlinhas):
            for j in range(self.ncolunas):
                if self.mapa2[i][j] == "<" or self.mapa2[i][j] == ">" or self.mapa2[i][j] == "A" or self.mapa2[i][j] == "V" or self.mapa2[i][j] == "R" or self.mapa2[i][j] == "P" or self.mapa2[i][j] == "B":
                    self.mapa2[i][j] = "."

    def criarMapaCaminhos(self, x, y):
        self.limparCaminhos()
        if dentroRect2(x, y, -10,135,310,320) or dentroRect2(x,y,515,640,310,320):
            novos = [(315 // ESCALA, 525 // ESCALA)]

        else:
            novos = [((y // ESCALA), (x // ESCALA))]
        self.mapa2[novos[0][0]][novos[0][1]] = "P"
        self.mapa2[self.y//ESCALA][self.x//ESCALA] = "R"
        processando = True
        tmp = 1
        while processando:
            nnovos = tmp
            tmp = 0
            for i in range(nnovos):
                if novos[0][0] ==(self.y//ESCALA) and novos[0][1] == (self.x//ESCALA):
                    processando = False
                    break
                if self.mapa2[novos[0][0]+1][novos[0][1]] == "." or self.mapa2[novos[0][0]+1][novos[0][1]] == " " or self.mapa2[novos[0][0]+1][novos[0][1]] == "@" or self.mapa2[novos[0][0]+1][novos[0][1]] == "R":
                    self.mapa2[novos[0][0]+1][novos[0][1]] = "A"
                    tmp += 1
                    novos.append((novos[0][0]+1, novos[0][1]))
                if self.mapa2[novos[0][0]][novos[0][1]-1] == "." or self.mapa2[novos[0][0]][novos[0][1]-1] == " " or self.mapa2[novos[0][0]][novos[0][1]-1] == "@" or self.mapa2[novos[0][0]][novos[0][1]-1] == "R":
                    self.mapa2[novos[0][0]][novos[0][1]-1] = ">"
                    tmp += 1
                    novos.append((novos[0][0], novos[0][1]-1))
                if self.mapa2[novos[0][0]-1][novos[0][1]] == "." or self.mapa2[novos[0][0]-1][novos[0][1]] == " " or self.mapa2[novos[0][0]-1][novos[0][1]] == "@" or self.mapa2[novos[0][0]-1][novos[0][1]] == "R":
                    self.mapa2[novos[0][0]-1][novos[0][1]] = "V"
                    tmp += 1
                    novos.append((novos[0][0]-1, novos[0][1]))
                if self.mapa2[novos[0][0]][novos[0][1] + 1] == "." or self.mapa2[novos[0][0]][novos[0][1] + 1] == " " or self.mapa2[novos[0][0]][novos[0][1] + 1] == "@" or self.mapa2[novos[0][0]][novos[0][1] + 1] == "R":
                    self.mapa2[novos[0][0]][novos[0][1] + 1] = "<"
                    tmp += 1
                    novos.append((novos[0][0], novos[0][1] + 1))
                novos.pop(0)

    def seguirCaminho(self):
        if self.mapa2[self.y//ESCALA][self.x//ESCALA] == "P" and naGrade(self.x, self.y,ESCALA-self.acceleration):
            self.velY = 0
            self.velX = 0
        elif self.mapa2[self.y//ESCALA][self.x//ESCALA] == "<" and naGrade(self.x, self.y,ESCALA-self.acceleration):
            self.velX = -self.acceleration
            self.velY = 0
        elif self.mapa2[self.y//ESCALA][self.x//ESCALA] == ">" and naGrade(self.x, self.y,ESCALA-self.acceleration):
            self.velX = +self.acceleration
            self.velY = 0
        elif self.mapa2[self.y//ESCALA][self.x//ESCALA] == "A" and naGrade(self.x, self.y,ESCALA-self.acceleration):
            self.velY = -self.acceleration
            self.velX = 0
        elif self.mapa2[self.y//ESCALA][self.x//ESCALA] == "V" and naGrade(self.x, self.y,ESCALA-self.acceleration):
            self.velY = +self.acceleration
            self.velX = 0
        else:
            pass

    def inteligencia(self, mapa2):
        if self.velX == 0 and self.velY == 0:
            for i in range(self.nlinhas):
                for j in range(self.ncolunas):
                    if mapa2.mapa[i][j] == ".":
                        randtmp = random.randint(0, 5)
                        if randtmp == 1:
                            self.criarMapaCaminhos(j*ESCALA, i*ESCALA)
        self.seguirCaminho()

    def tick(self, pacman, mapa):
        self.inteligencia(mapa)
        if not mapa.colisionRectMap(self.x + self.velX, self.y, ESCALA-self.acceleration+1, "Ghost"):
            self.x += self.velX
        if not mapa.colisionRectMap(self.x, self.y + self.velY, ESCALA-self.acceleration+1, "Ghost"):
            self.y += self.velY

    def display(self):
        screen.blit(self.image, (self.x, self.y))

    def displayMapa(self):
        for i in range(self.nlinhas):
            for j in range(self.ncolunas):
                if self.mapa2[i][j] == "#":
                    screen.blit(self.wallSkin, (j * ESCALA, i * ESCALA))
                elif self.mapa2[i][j] == "P":
                    screen.blit(self.pacSkin, (j * ESCALA, i * ESCALA))
                elif self.mapa2[i][j] == "<":
                    screen.blit(self.setaOeste, (j * ESCALA, i * ESCALA))
                elif self.mapa2[i][j] == ">":
                    screen.blit(self.setaLeste, (j * ESCALA, i * ESCALA))
                elif self.mapa2[i][j] == "A":
                    screen.blit(self.setaNorte, (j * ESCALA, i * ESCALA))
                elif self.mapa2[i][j] == "V":
                    screen.blit(self.setaSul, (j * ESCALA, i * ESCALA))


# setup variaveis e constantes do pygame
food_sound = mixer.Sound("eat.wav")
font = pygame.font.Font('freesansbold.ttf', ESCALA)
fontGameOver = pygame.font.Font('freesansbold.ttf', 70)
fontGameOverOther = pygame.font.Font('freesansbold.ttf', 35)
scoreTextX = 10
scoreTextY = 10
f = open("mapa.txt", "r")
mapachar = []
# carregar mapachar
for i in range(altura):
    linha = []
    for j in range(largura):
        s = f.read(1)
        s.split()
        linha.append(s)
    mapachar.append(linha)

# criar e iniciar objetos
mapa1 = Mapa(mapachar, altura, largura)
player = Pacman
blueGhost = BlueGhost(mapachar)
redGhost = RedGhost(mapachar, altura, largura)
orangeGhost = OrangeGhost(mapachar,altura, largura)
greenGhost = GreenGhost(mapachar,altura, largura)
mapa1.inicializarObjetos(player, blueGhost, redGhost,orangeGhost,greenGhost)
clock = pygame.time.Clock()

def inicializar():
    global lives, score_value, mapachar,mapa1,player,blueGhost,redGhost,orangeGhost,greenGhost,pause, sound
    f = open("mapa.txt", "r")
    mapachar = []
    # carregar mapachar
    for i in range(altura):
        linha = []
        for j in range(largura):
            s = f.read(1)
            s.split()
            linha.append(s)
        mapachar.append(linha)
    lives = 4
    score_value = 0
    mapa1 = Mapa(mapachar, altura, largura)
    player = Pacman
    blueGhost = BlueGhost(mapachar)
    redGhost = RedGhost(mapachar, altura, largura)
    orangeGhost = OrangeGhost(mapachar, altura, largura)
    greenGhost = GreenGhost(mapachar, altura, largura)
    mapa1.inicializarObjetos(player, blueGhost, redGhost, orangeGhost, greenGhost)
    player.request = "null"
    player.velX=0
    player.velY=0
    player.ivuneravelTime =5
    pause=True
    mixer.music.load("pacman.mp3")
    if sound:
        mixer.music.play(-1)


async def run():
    global running, playing, win, lose, score_value, lives, pause, sound, debug, ativardebug, newWalk
    # rodando a tela
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    playing = True
                    win = False
                    lose = False
                    inicializar()
        # rodando o jogo
        while playing:
            # fps = 30
            clock.tick(fps)
            # botoes
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    playing = False
                    pygame.quit()
                # pressionou teclado
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and newWalk:
                        keys[0] += 1
                        if keys[0] == 1:
                            player.velX += player.acelleration
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and newWalk:
                        keys[2] += 1
                        if keys[2] == 1:
                            player.velX += -player.acelleration
                    elif (event.key == pygame.K_UP or event.key == pygame.K_w) and newWalk:
                        keys[1] += 1
                        if keys[1] == 1:
                            player.velY += -player.acelleration
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and newWalk:
                        keys[3] += 1
                        if keys[3] == 1:
                            player.velY += player.acelleration
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and not newWalk:
                        player.request="leste"
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and not newWalk:
                        player.request="oeste"
                    elif (event.key == pygame.K_UP or event.key == pygame.K_w) and not newWalk:
                        player.request="norte"
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and not newWalk:
                        player.request="sul"
                    elif event.key == pygame.K_k:
                        if debug:
                            debug = False
                            ativardebug=0
                        elif not debug:
                            ativardebug+=1
                    elif event.key == pygame.K_m:
                        if ativardebug == 1:
                            ativardebug+=1
                        else:
                            ativardebug=0
                        if sound == False:
                            sound = True
                            mixer.music.unpause()
                        elif sound == True:
                            sound = False
                            mixer.music.pause()
                    elif event.key == pygame.K_z:
                        if ativardebug == 2:
                            ativardebug+=1
                            debug=True
                        else:
                            ativardebug=0
                    elif event.key == pygame.K_p:
                        if pause:
                            if sound:
                                mixer.music.unpause()
                            pause = False

                        else:
                            pause = True
                            mixer.music.pause()
                    elif event.key == pygame.K_c:
                        if newWalk:
                            player.request="null"
                            newWalk = False

                        else:
                            player.velX=0
                            player.velY=0
                            keys[0]=0
                            keys[1]=0
                            keys[2] = 0
                            keys[3] = 0
                            newWalk = True
                # soltou teclado
                if event.type == pygame.KEYUP:
                    if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and newWalk:
                        keys[0] -= 1
                        if keys[0] == 0:
                            player.velX -= player.acelleration
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and newWalk:
                        keys[2] -= 1
                        if keys[2] == 0:
                            player.velX -= -player.acelleration
                    elif (event.key == pygame.K_UP or event.key == pygame.K_w) and newWalk:
                        keys[1] -= 1
                        if keys[1] == 0:
                            player.velY -= -player.acelleration
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and newWalk:
                        keys[3] -= 1
                        if keys[3] == 0:
                            player.velY -= player.acelleration
            # ticks
            if not pause:
                player.tick(player, mapa1)
                blueGhost.tick(mapa1)
                redGhost.tick(player,mapa1)
                orangeGhost.tick(player, mapa1)
                greenGhost.tick(player, mapa1)

            # colisoes com fantasmas
            if (colideRect(player, ESCALA, blueGhost, ESCALA) or colideRect(player, ESCALA, redGhost, ESCALA) or colideRect(player, ESCALA, orangeGhost, ESCALA) or colideRect(player, ESCALA, greenGhost, ESCALA)) and player.ivuneravelTime == 0 and not debug:
                lives -= 1
                player.ivuneravelTime = 300

            # renders
            screen.fill((0, 0, 0))
            mapa1.display()
            redGhost.display()
            if debug:
                redGhost.displayMapa()
            blueGhost.display()
            blueGhost.displaySensores(mapa1)
            if debug:
                orangeGhost.displayMapa()
            orangeGhost.display()
            if debug:
                greenGhost.displayMapa()
            greenGhost.display()
            player.display(player)
            player.displaySensores(player,mapa1)
            show_hud(0, 0)
            if pause:
                screen.blit(fontGameOver.render("       Pause", True, (200, 10, 10)), (WIDTH // 7, HEIGHT * 2 // 5))
                screen.blit(fontGameOverOther.render("Aperte \"P\" para despausar", True, (200, 200, 200)),
                            (WIDTH // 7 + 50, (HEIGHT * 2 // 5) + 100))
                screen.blit(fontGameOverOther.render("Aperte \"C\" para mudar a forma", True, (200, 200, 200)),
                            (WIDTH // 7, (HEIGHT * 2 // 5) + 100+40))
                screen.blit(fontGameOverOther.render("de andar", True, (200, 200, 200)),
                            (WIDTH // 7+160, (HEIGHT * 2 // 5) + 100 + 40+40))


            # ganhar o jogo
            if score_value == 176:
                playing = False
                win = True

            # perder o jogo
            if lives <= 0:
                playing = False
                lose = True

            # ganhou o jogo
            if win:
                screen.blit(fontGameOver.render("Você Venceu!!!", True, (200, 10, 10)), (WIDTH // 7, HEIGHT * 2 // 5))
                screen.blit(fontGameOverOther.render("Aperte \"R\" para reiniciar", True, (200, 200, 200)),
                            (WIDTH // 7 + 50, (HEIGHT * 2 // 5) + 100))
                if sound:
                    mixer.music.load("win.mp3")
                    mixer.music.play()
                pygame.display.update()

            # perdeu o jogo
            if lose:
                screen.blit(fontGameOver.render("Você Perdeu :(", True, (200, 10, 10)), (WIDTH // 7, HEIGHT * 2 // 5))
                screen.blit(fontGameOverOther.render("Aperte \"R\" para reiniciar", True, (200, 200, 200)), (WIDTH // 7 + 50, (HEIGHT * 2 // 5)+100))
                if sound:
                    mixer.music.load("lose.mp3")
                    mixer.music.play()
                pygame.display.update()

            # atualizar tela
            pygame.display.update()
            await asyncio.sleep(0)
        await asyncio.sleep(0)


asyncio.run(run())


# cd ..
# python -m pygbag Pacman

# zip da pasta web
# envia para itch.io