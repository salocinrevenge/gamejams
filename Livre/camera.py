from algelin import toIsometric
class Camera():
    def __init__(self, mundo, pos) -> None:
        self.mundo = mundo
        self.x = pos[0]
        self.y = pos[1]
        
    def tick(self):
        pass
    
    def render(self, screen, imagem, pos):
        x,y = toIsometric(pos[0], pos[1])
        screen.blit(imagem, (x * 32+self.x, y * 32+self.y))
        
    
    def input(self, evento):
        pass