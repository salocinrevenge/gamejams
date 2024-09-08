import pygame
class Semente():
    def __init__(self) -> None:
        pass

    def renderItem(self, screen,x,y,escala):
        x = x+escala//2
        y = y+escala//2
        pygame.draw.ellipse(screen, (100, 50, 0), pygame.Rect(x+2, y+2, 2*escala, 4*escala))
        pygame.draw.ellipse(screen, (100, 50, 0), pygame.Rect(x+2, y+14, 2*escala, 4*escala))
        pygame.draw.ellipse(screen, (100, 50, 0), pygame.Rect(x+14, y+2, 2*escala, 4*escala))
        pygame.draw.ellipse(screen, (100, 50, 0), pygame.Rect(x+8, y+8, 2*escala, 4*escala))
        pygame.draw.ellipse(screen, (100, 50, 0), pygame.Rect(x+8, y+22, 2*escala, 4*escala))
        pygame.draw.ellipse(screen, (100, 50, 0), pygame.Rect(x+20, y+8, 2*escala, 4*escala))
        pygame.draw.ellipse(screen, (100, 50, 0), pygame.Rect(x+14, y+14, 2*escala, 4*escala))
