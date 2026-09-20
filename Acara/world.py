import pyray as rl

from camera import Camera
from building import Building
from infos import resources_flux, buildings, upgrades_buildings, resources

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

        # carrega a sprite sheet
        self.img_sprite_sheet_buildings = rl.load_texture(b"assets/buildings.png")
        self.img_sprite_sheet_resources = rl.load_texture(b"assets/resources.png")


    def tick(self):
        self.resources_timer += 1
        if self.resources_timer >= self.time_to_generate_resources:
            self.resources_timer = 0
            self.resources_timer2 += 1
            
            # Inicializa os fluxos deste ciclo
            generating = {"energy": 0, "people": 0}
            consumed = {"energy": 0, "people": 0}
            
            # Guarda a capacidade de fluxo do ciclo anterior para checar se as máquinas podem ligar
            generated = {"energy": self.resources_storage.get("energy", 0), "people": self.resources_storage.get("people", 0)}

            # Zera completamente todo o armazenamento (vamos recalcular do zero lendo as construções)
            for res in self.resources_storage:
                self.resources_storage[res] = 0

            # 1. PRIMEIRO PASSO: Calcula a capacidade MÁXIMA de armazenamento físico do mapa
            for x in range(self.width):
                for y in range(self.height):
                    if self.map[y][x].parent is not None or self.map[y][x].id == "ground":
                        continue
                    
                    id = self.map[y][x].id
                    b_storage = dict(self.map[y][x].info[id].get("storage", {}))
                    
                    if self.map[y][x].active_upgrade:
                        upg_data = upgrades_buildings.get(id, {}).get(self.map[y][x].active_upgrade, {})
                        for k, v in upg_data.get("storage", {}).items():
                            b_storage[k] = b_storage.get(k, 0) + v
                            
                    for res, amount in b_storage.items():
                        if res not in resources_flux:
                            self.resources_storage[res] = self.resources_storage.get(res, 0) + amount

            # 2. SEGUNDO PASSO: Produção e consumo das máquinas
            for x in range(self.width):
                for y in range(self.height):
                    if self.map[y][x].parent is not None or self.map[y][x].id == "ground":
                        continue
                    
                    id = self.map[y][x].id
                    delay = self.map[y][x].info[id].get("delay", 1)
                    
                    b_consumes = dict(self.map[y][x].info[id].get("consumes", {}))
                    b_produces = dict(self.map[y][x].info[id].get("produces", {}))
                    
                    # Combina com Upgrades se houver
                    if self.map[y][x].active_upgrade:
                        upg_data = upgrades_buildings.get(id, {}).get(self.map[y][x].active_upgrade, {})
                        for k, v in upg_data.get("consumes", {}).items(): b_consumes[k] = b_consumes.get(k, 0) + v
                        for k, v in upg_data.get("produces", {}).items(): b_produces[k] = b_produces.get(k, 0) + v

                    has_enough_resources = True
                    missing = []

                    # Verifica se tem recursos de Fluxo e Físicos suficientes para rodar agora
                    for res, amount in b_consumes.items():
                        if res in resources_flux:
                            if consumed.get(res, 0) + amount > generated.get(res, 0):
                                has_enough_resources = False
                                missing.append(res)
                        elif amount < 0:
                            # Se for negativo (ex: consome -0.05 esgoto = gera esgoto), confere se tem espaço físico pra guardar
                            if self.resources.get(res, 0) + abs(amount) > self.resources_storage.get(res, 0):
                                has_enough_resources = False
                                missing.append(res)
                        elif self.resources.get(res, 0) < amount:
                            has_enough_resources = False
                            missing.append(res)

                    self.map[y][x].is_working = has_enough_resources
                    self.map[y][x].missing_resources = missing

                    if not has_enough_resources:
                        continue 

                    # Consumo e Produção dos FLUXOS (Acontece constantemente)
                    for res, amount in b_consumes.items():
                        if res in resources_flux:
                            consumed[res] = consumed.get(res, 0) + amount
                            
                    for res, amount in b_produces.items():
                        if res in resources_flux:
                            generating[res] = generating.get(res, 0) + amount

                    # Consumo e Produção FÍSICA (Acontece quando bate o Timer)
                    self.map[y][x].timer += 1
                    if self.map[y][x].timer >= delay:
                        self.map[y][x].timer = 0  
                        
                        for res, amount in b_consumes.items():
                            if res not in resources_flux:
                                if amount > 0:
                                    self.resources[res] -= amount
                                else:
                                    self.resources[res] += abs(amount) # Adiciona ao estoque pq o consumo é negativo

                        for res, amount in b_produces.items():
                            if res not in resources_flux:
                                if res not in self.resources:
                                    self.resources[res] = 0
                                if self.resources_storage.get(res, 0) >= self.resources.get(res, 0) + amount:
                                    self.resources[res] += amount

            # 3. TERCEIRO PASSO: Consolida os Fluxos na UI
            for res, amount in consumed.items():
                self.resources[res] = amount
            for res, amount in generating.items():
                self.resources_storage[res] = amount

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

    def place_building(self, building_selected, free=False):
        if not building_selected:
            return False  # Nenhuma ação de seleção ativa

        # Verifica colisões (limites do mapa e se está ocupado)
        if building_selected.x < 0 or building_selected.y < 0 or \
           building_selected.x + building_selected.width > self.width or \
           building_selected.y + building_selected.height > self.height:
            return False

        for i in range(building_selected.height):
            for j in range(building_selected.width):
                if self.map[building_selected.y + i][building_selected.x + j].id != "ground":
                    return False  # Posição já ocupada

        costs = buildings[building_selected.id].get("cost", {})
        
        # Só verifica e cobra custos se não for 'free' (se for move, free será True)
        if not free:
            for resource, amount in costs.items():
                if self.game_manager.hud.resources.get(resource, 0) < amount:
                    return False  # Não tem recursos suficientes
            
            for resource, amount in costs.items():
                self.game_manager.hud.resources[resource] -= amount

        # Coloca no mapa
        self.map[building_selected.y][building_selected.x] = building_selected
        for i in range(building_selected.height):
            for j in range(building_selected.width):
                if i == 0 and j == 0:
                    continue
                self.map[building_selected.y + i][building_selected.x + j] = Building(
                    building_selected.id, 
                    building_selected.x + j, 
                    building_selected.y + i, 
                    parent=building_selected, 
                    shift_sprite_sheet=rl.Vector2(j, i)
                )

        return True

    def get_parent_building(self, x, y):
        # Retorna a construção principal, mesmo que clique numa parte de uma 3x3
        building = self.map[y][x]
        if building.id == "ground":
            return None
        if building.parent:
            return building.parent
        return building

    def destroy_building(self, x, y):
        parent = self.get_parent_building(x, y)
        if not parent:
            return False

        # Substitui todos os blocos ocupados pela construção de volta por "ground"
        for i in range(parent.height):
            for j in range(parent.width):
                self.map[parent.y + i][parent.x + j] = Building("ground", parent.x + j, parent.y + i)
        return True

    def pick_up_building(self, x, y):
        parent = self.get_parent_building(x, y)
        if not parent:
            return None
        
        # Salva o ID da construção que estava lá para recriar no mouse
        id_to_move = parent.id
        self.destroy_building(x, y) # Limpa ela do mapa
        
        return Building(id_to_move, 0, 0) # Retorna uma nova pra ficar "na mão" do jogador