from algelin import toIsometric

class Camera():
    def __init__(self, mundo, pos) -> None:
        self.mundo = mundo
        self.x = pos[0]
        self.y = pos[1]
        self.target = None
        
    def setTarget(self, target):
        self.target = target
        
    def tick(self):
        if self.target:
            deslSala = self.target.mundo.salaAtual.deslocamentoSala()
            print(deslSala)
            
            self.x,self.y = toIsometric(-((deslSala[0]+self.target.x)*32), -((deslSala[1]+self.target.y)*32))
            self.x += 350
            self.y += 350
    
    def render(self, screen, imagem, pos):
        x,y = toIsometric(pos[0], pos[1])
        screen.blit(imagem, (x * 32+self.x, y * 32+self.y))
        
    
    def input(self, evento):
        pass