class Personagem:
    def __init__(self, x, y, mundo) -> None:
        self.x = x
        self.y = y
        self.mundo = mundo
        self.barco = None

    def tick(self):
        if self.barco:
            self.barco.setPos(self.x, self.y)

    def render(self, screen, camera, deslocamento):
        if self.barco:
            self.barco.render(screen, camera, deslocamento)

    def input(self, evento):
        pass
    
    def setPos(self, x, y):
        self.x = x
        self.y = y
        
    def setBarco(self, barco):
        self.barco = barco
        
    def largarBarco(self):
        barco = self.barco
        self.barco = None
        return barco