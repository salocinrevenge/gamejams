import pyray as rl
import json
import os

from hud import HUD
from world import World
from camera import Camera
from building import Building
from infos import resources
from meteor_event import MeteorEvent
from endgame_manager import EndgameManager

class GameManager:

    def start_resources(self):
        self.resources = {
            "energy": 0,
            "people": 4,
            "water": 100,
            "food": 50,
            "sewage": 0,
            "ore": 2000,
            "iron": 1000,
            "silicon": 500,
        }

        self.technologies = set(["mining", "fotovoltaic"])  # Tecnologias desbloqueadas no início do jogo
    

    def __init__(self):
        escala = 64
        height = 100
        width = 100
        self.start_resources()
        self.paused = False  # Estado de pausa do jogo
        self.time_to_generate_resources = 5  # Tempo em ticks
        self.resources_storage = {resource: 0 for resource in resources.keys()}
        self.camera = Camera(self, pos=rl.Vector2(-(width//2-8), -(height//2-5)), escala=escala)
        self.world = World(self, self.camera, width=width, height=height, escala=escala)
        self.hud = HUD(self, resources=self.resources)
        self.meteor_event = MeteorEvent(self)
        self.endgame = EndgameManager(self)

        self.should_restart = False
        self.sim_speed = 1.0           # Velocidade atual (0.5x, 1x, 2x, 4x)
        self.ticks_accumulator = 0.0   # Acumula frações de frame para velocidades lentas ou rápidas
        self.run_ticks = 0             # Tempo total de jogo (em ticks)
        self.history_timer = 0         # Temporizador para salvar o histórico
        self.resources_history = []    # Fila com o estado dos recursos no último minuto (60 segundos)


    def tick(self):
        self.endgame.tick()
        self.camera.tick()
        
        def advance_sim():
            self.world.tick()
            if self.endgame.state == "NONE":
                self.meteor_event.tick()
                
            self.run_ticks += 1
            
            # --- Controle do Histórico a cada segundo (60 frames) ---
            self.history_timer += 1
            if self.history_timer >= 60:
                self.history_timer = 0
                self.resources_history.append(self.resources.copy())
                if len(self.resources_history) > 60: # Limita a 60 memórias (último minuto)
                    self.resources_history.pop(0)

        # Se não estiver pausado e nem em cena bloqueada, roda o loop X vezes por frame
        if not self.paused and self.endgame.state in ["NONE", "WAITING"]:
            self.ticks_accumulator += self.sim_speed
            while self.ticks_accumulator >= 1.0:
                advance_sim()
                self.ticks_accumulator -= 1.0

        self.hud.tick()

    def render(self):
        self.world.render()
        self.meteor_event.render()
        
        # Esconde o HUD nos fade outs ou se for tela de vitória
        if self.endgame.state in ["NONE", "AIMING", "WAITING"]:
            self.hud.render()
            
        self.endgame.render() # UI de finalização deve se sobrepor

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

    
