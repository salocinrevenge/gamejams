import pyray as rl

from hud import HUD
from world import World
from camera import Camera

from infos import resources

class GameManager:

    resources = {
        "energy": 0,
        "people": 4,
        "water": 100,
        "food": 50,
        "sewage": 0,
        "ore": 2000,
        "iron": 1000,
        "silicon": 500,
    }
    

    def __init__(self):
        escala = 64
        height = 100
        width = 100
        self.time_to_generate_resources = 5  # Tempo em ticks
        self.resources_storage = {resource: 0 for resource in resources.keys()}
        self.camera = Camera(self, pos=rl.Vector2(-(width//2-8), -(height//2-5)), escala=escala)
        self.world = World(self, self.camera, width=width, height=height, escala=escala)
        self.hud = HUD(self, resources=self.resources)

    def tick(self):
        self.camera.tick()
        self.world.tick()
        self.hud.tick()

    def render(self):
        self.world.render()
        self.hud.render()

    def on_close(self):
        self.world.on_close()

    
