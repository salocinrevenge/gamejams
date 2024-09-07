

class Personagem:
    def __init__(self, x, y, mundo) -> None:
        self.x = x
        self.y = y
        self.mundo = mundo

    def tick(self):
        pass

    def render(self, screen, camera):
        pass

    def input(self, evento):
        pass
    
    def setPos(self, x, y):
        print("setando posicao para ", x, y)
        self.x = x
        self.y = y