import pyray as rl
import json
import os

from hud import HUD
from world import World
from camera import Camera
from building import Building
from infos import resources
from meteor_event import MeteorEvent

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

    technologies = set(["mining", "fotovoltaic"])  # Tecnologias desbloqueadas no início do jogo
    

    def __init__(self):
        escala = 64
        height = 100
        width = 100
        self.paused = False  # Estado de pausa do jogo
        self.time_to_generate_resources = 5  # Tempo em ticks
        self.resources_storage = {resource: 0 for resource in resources.keys()}
        self.camera = Camera(self, pos=rl.Vector2(-(width//2-8), -(height//2-5)), escala=escala)
        self.world = World(self, self.camera, width=width, height=height, escala=escala)
        self.hud = HUD(self, resources=self.resources)
        self.meteor_event = MeteorEvent(self)

    def tick(self):
        self.camera.tick()
        if not self.paused:
            self.world.tick()
            self.meteor_event.tick()
        self.hud.tick()

    def render(self):
        self.world.render()
        self.meteor_event.render()
        self.hud.render()

    def on_close(self):
        self.world.on_close()

    def save_game(self):
        data = {
            "resources": self.resources,
            "technologies": list(self.technologies),
            "camera": {"x": self.camera.pos.x, "y": self.camera.pos.y, "zoom": self.camera.zoom},
            "buildings": []
        }
        for y in range(self.world.height):
            for x in range(self.world.width):
                b = self.world.map[y][x]
                # Só salva a construção 'Pai' para não duplicar os filhos no save
                if b.id != "ground" and b.parent is None:
                    data["buildings"].append({
                        "id": b.id, "x": b.x, "y": b.y, 
                        "timer": getattr(b, "timer", 0), 
                        "active_upgrade": getattr(b, "active_upgrade", None)
                    })
        with open("savegame.json", "w") as f:
            json.dump(data, f)
        print("Jogo Salvo com Sucesso!")

    def load_game(self):
        if not os.path.exists("savegame.json"):
            print("Nenhum save encontrado.")
            return
            
        with open("savegame.json", "r") as f:
            data = json.load(f)
        
        self.resources.update(data.get("resources", {}))
        self.technologies = set(data.get("technologies", []))
        
        cam = data.get("camera", {})
        self.camera.pos.x = cam.get("x", self.camera.pos.x)
        self.camera.pos.y = cam.get("y", self.camera.pos.y)
        self.camera.zoom = cam.get("zoom", self.camera.zoom)
        
        # Limpa todo o mapa
        for y in range(self.world.height):
            for x in range(self.world.width):
                self.world.map[y][x] = Building("ground", x, y)
                
        # Reconstrói e carrega as máquinas
        for b_data in data.get("buildings", []):
            new_b = Building(b_data["id"], b_data["x"], b_data["y"])
            new_b.timer = b_data.get("timer", 0)
            new_b.active_upgrade = b_data.get("active_upgrade", None)
            self.world.place_building(new_b, free=True)
            
        print("Jogo Carregado com Sucesso!")

    def pause_toggle(self):
        self.paused = not self.paused

    
