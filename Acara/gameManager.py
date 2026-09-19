import pyray as rl

from world import World
from camera import Camera

class GameManager:
    def __init__(self):
        escala = 64
        height = 100
        width = 100
        # self.camera = Camera(pos=rl.Vector2((width//2), (height//2)), escala=escala)
        self.camera = Camera(pos=rl.Vector2(0, 0), escala=escala)
        self.world = World(self.camera, width=width, height=height, escala=escala)

    def tick(self):
        self.camera.tick()
        self.world.tick()

    def render(self):
        self.world.render()