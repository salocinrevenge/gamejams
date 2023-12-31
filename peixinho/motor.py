import pygame
import time
import asyncio
from menu import Menu
from excessoes.Win import Win

class Coracao():

    def __init__(self) -> None:
        pygame.init()

        # Definir as dimensões da janela
        dimensoes = pygame.display.get_desktop_sizes()[0]
        self.WINDOW_WIDTH = dimensoes[0] * 0.7
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = dimensoes[1] * 0.7
        self.WINDOW_HEIGHT = 800+100
        self.FPS_PADRAO = 60.0
        self.UPDATE_CAP = 1.0/self.FPS_PADRAO
        self.menu = Menu()
        # Criar a janela
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Ribopolho chega em Marte") # titulo da janela
        


    async def run(self):
        self.running = True
        render = False
        firstTime = 0
        lastTime = time.time()  # retorna o tempo atual em segundos
        passedTime = 0
        unprocessedTime = 0
        frameTime = 0
        frames = 0
        fps = 0

        while self.running:
                render = False
                firstTime = time.time()
                passedTime = firstTime - lastTime   # tempo que passou desde a ultima vez que o loop foi executado
                lastTime = firstTime            # atualiza o tempo da ultima vez que o loop foi executado

                unprocessedTime += passedTime  # tempo nao processado
                frameTime += passedTime

                # enquanto nao processou td q deveria (devido a lag em render ou coisas assim)
                while unprocessedTime >= self.UPDATE_CAP:
                    # Isso garante que o tempo de atualizacao seja constante
                    # e nao dependa do tempo de renderizacao. Igualando o 
                    # jogo para todos os computadores, apenas aumentando o
                    # fps para computadores mais potentes
                    unprocessedTime -= self.UPDATE_CAP  # Tempo comido
                    render = True

                    try:
                        self.tick()
                    except Win as e:
                        print(e.message)
                        self.running = False
                        self.dispose()
                        return

                    if frameTime >= 1.0:
                            frameTime = 0
                            fps = frames
                            frames = 0
                            # print("FPS: " + str(fps))

                # Depois de processar o tempo, renderiza
                if render:
                    self.render(self)
                    frames += 1
                else:
                    time.sleep(0.001)
                await asyncio.sleep(0)
                
        self.dispose()
      
    def tick(self): # metodo chamado a cada frame
        self.input()
        self.menu.tick()
        # mostra a coordenada do mouse
        # print(pygame.mouse.get_pos())

    def render(self, gc): # metodo chamado a cada frame
        # Limpar a telaa
        self.screen.fill((0,0,0))

        # Renderizar o mapa
        self.menu.render(self.screen)

        # Atualizar a tela
        pygame.display.flip()

    def input(self):
        # Verificar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            self.menu.input(event)

    def dispose(self):      # metodo chamado quando o jogo fecha
            pass

Coracao()
