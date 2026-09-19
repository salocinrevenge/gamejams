import pyray as rl

from camera import Camera
from building import Building

from resources import resources_flux

class World:
    def __init__(self, game_manager, camera: Camera, width=100, height=100, escala=64) -> None:
        self.game_manager = game_manager
        self.camera = camera
        self.width = width
        self.height = height
        self.escala = escala
        self.resources = self.game_manager.resources
        self.resources_storage = self.game_manager.resources_storage
        self.time_to_generate_resources = self.game_manager.time_to_generate_resources
        self.resources_timer = 0
        self.resources_timer2 = 0

        self.map = [[ Building("ground", x, y) for x in range(width)] for y in range(height)]
        self.load_game()  # Tenta carregar o jogo salvo, se existir

        # carrega a sprite sheet
        self.img_sprite_sheet_buildings = rl.load_texture(b"assets/buildings.png")
        self.img_sprite_sheet_resources = rl.load_texture(b"assets/resources.png")


    def tick(self):
        self.resources_timer += 1
        if self.resources_timer >= self.time_to_generate_resources:
            self.resources_timer = 0
            self.resources_timer2 += 1
            generating={"energy": 0, "people": 0}
            generated={"energy": self.resources_storage.get("energy", 0), "people": self.resources_storage.get("people", 0)}
            consumed={"energy": 0, "people": 0}

            # Reset storage counts
            last_storage = self.resources_storage.copy()
            for resource in self.resources_storage:
                self.resources_storage[resource] = 0

            # Gera novos recursos
            for x in range(self.width):
                for y in range(self.height):
                    if self.map[y][x].parent is not None:
                        continue  # Pula se for uma construção filha (não principal)

                    id = self.map[y][x].id

                    # Pega o delay e os custos da construção
                    delay = self.map[y][x].info[id].get("delay", 1)
                    consumes = self.map[y][x].info[id].get("consumes", {})
                    has_enough_resources = True

                    # 1. Verifica se há recursos suficientes (físicos e fluxo) para operar neste tick
                    for resource, amount in consumes.items():
                        if resource in resources_flux:
                            if consumed.get(resource, 0) + amount > generated.get(resource, 0):
                                has_enough_resources = False
                                break
                        elif amount < 0:  # Se for um recurso que é gerado (como sewage), precisa ter espaço de armazenamento
                            if self.resources.get(resource, 0) + amount > last_storage.get(resource, 0):
                                has_enough_resources = False
                                break
                        elif self.resources.get(resource, 0) < amount:
                            has_enough_resources = False
                            break

                    # Se faltar energia, pessoas ou material físico, o timer congela e não avança
                    if not has_enough_resources:
                        continue 

                    # 2. Consome os recursos de FLUXO (energia/pessoas) para se manter funcionando neste tick
                    for resource, amount in consumes.items():
                        if resource in resources_flux:
                            consumed[resource] += amount

                    # 3. Avança o timer individual da construção
                    self.map[y][x].timer += 1

                    # 4. Se o timer atingiu o delay, consome materiais físicos e produz
                    if self.map[y][x].timer >= delay:
                        self.map[y][x].timer = 0  # Reseta o timer para o próximo ciclo
                        
                        # Consome recursos físicos permanentemente
                        for resource, amount in consumes.items():
                            if resource not in resources_flux:
                                self.resources[resource] -= amount

                        # Gera os recursos produzidos
                        produces = self.map[y][x].info[id].get("produces", {})
                        for resource, amount in produces.items():
                            if resource in resources_flux:
                                generating[resource] = generating.get(resource, 0) + amount
                                continue
                            if resource not in self.resources:
                                self.resources[resource] = 0
                            if last_storage.get(resource, 0) > self.resources[resource] + amount:
                                self.resources[resource] += amount

                    # O cálculo de armazenamento (storage) continua ocorrendo independentemente do timer
                    storage = self.map[y][x].info[id].get("storage", {})
                    for resource, amount in storage.items():
                        if resource not in self.resources_storage:
                            self.resources_storage[resource] = 0
                        self.resources_storage[resource] += amount

            for resource in generating:
                self.resources_storage[resource] = generating[resource]
            for resource in consumed:
                self.resources[resource] = consumed[resource]

    def get_color(self, id):
        if id == 0:
            return rl.Color(100, 20, 20, 255)
        elif id == 1:
            return rl.GREEN
        elif id == 2:
            return rl.BLUE
        else:
            return rl.RED

    def render(self):
        for x in range(self.width):
            for y in range(self.height):
                self.camera.draw_building(self.img_sprite_sheet_buildings, self.map[y][x])
    

    def on_close(self):
        rl.unload_texture(self.img_sprite_sheet_buildings)
        rl.unload_texture(self.img_sprite_sheet_resources)

    def save_game(self):
            # Salva o estado do jogo em um arquivo save.txt
            with open("save.txt", "w") as f:
                f.write(f"{self.camera.pos.x},{self.camera.pos.y},{self.camera.zoom}\n")
                for y in range(self.world.height):
                    for x in range(self.world.width):
                        building = self.world.map[y][x]
                        f.write(f"{building.id},{building.x},{building.y}\n")
    
    def load_game(self):
        # Carrega o estado do jogo a partir de um arquivo save.txt
        try:
            with open("save.txt", "r") as f:
                lines = f.readlines()
                camera_data = lines[0].strip().split(",")
                self.camera.pos.x = float(camera_data[0])
                self.camera.pos.y = float(camera_data[1])
                self.camera.zoom = float(camera_data[2])
                for line in lines[1:]:
                    building_data = line.strip().split(",")
                    id = building_data[0]
                    x = int(building_data[1])
                    y = int(building_data[2])
                    self.map[y][x] = Building(id, x, y)
        except FileNotFoundError:
            print("No save file found. Starting a new game.")

    def place_building(self, building_selected):
        if not building_selected:
            return False  # Nenhuma ação de seleção ativa

        # Verifica primeiro
        if self.map[building_selected.y][building_selected.x].id != "ground":
            return False  # Posição já ocupada
        for i in range(building_selected.height):
            for j in range(building_selected.width):
                if i == 0 and j == 0:
                    continue  # Pula a posição principal da construção

                if self.map[building_selected.y + i][building_selected.x + j].id != "ground":
                    return False  # Posição já ocupada

        costs = Building.info[building_selected.id].get("cost", {})
        # Ve se consegue pagar os custos
        for resource, amount in costs.items():
            if self.game_manager.hud.resources.get(resource, 0) < amount:
                return False  # Não tem recursos suficientes

            
        self.map[building_selected.y][building_selected.x] = building_selected
        for i in range(building_selected.height):
            for j in range(building_selected.width):
                if i == 0 and j == 0:
                    continue  # Pula a posição principal da construção
                
                self.map[building_selected.y + i][building_selected.x + j] = Building(
                    building_selected.id, 
                    building_selected.x + j, 
                    building_selected.y + i, 
                    parent=building_selected, 
                    shift_sprite_sheet=rl.Vector2(
                        j, 
                        i
                    )
                )

        # Paga os custos
        for resource, amount in costs.items():
            self.game_manager.hud.resources[resource] -= amount
        return True