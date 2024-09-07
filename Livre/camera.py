class Camera():
    def __init__(self, mundo) -> None:
        self.mundo = mundo
        
    def tick(self):
        pass
    
    def render(self, screen, imagem, pos):
        screen.blit(imagem, (pos[0] * 64, pos[1] * 64))
        
    
    def input(self, evento):
        pass