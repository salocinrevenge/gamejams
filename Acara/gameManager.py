import pyray as rl

from hud import HUD
from world import World
from camera import Camera

class GameManager:
    def __init__(self):
        escala = 64
        height = 100
        width = 100
        # self.camera = Camera(pos=rl.Vector2((width//2), (height//2)), escala=escala)
        self.camera = Camera(self, pos=rl.Vector2(-(width//2-8), -(height//2-5)), escala=escala)
        self.world = World(self.camera, width=width, height=height, escala=escala)
        self.hud = HUD(self)

    def tick(self):
        self.camera.tick()
        self.world.tick()
        self.hud.tick()

    def render(self):
        self.world.render()
        self.hud.render()

    def on_close(self):
        self.world.on_close()

    
