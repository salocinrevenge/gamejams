import pyray as rl

from camera import Camera
from building import Building

class World:
    def __init__(self, camera: Camera, width=100, height=100, escala=64) -> None:
        self.camera = camera
        self.width = width
        self.height = height
        self.escala = escala

        self.map = [[ Building("ground", x, y) for x in range(width)] for y in range(height)]
        self.load_game()  # Tenta carregar o jogo salvo, se existir

        # carrega a sprite sheet
        self.img_sprite_sheet_buildings = rl.load_texture(b"assets/buildings.png")
        self.img_sprite_sheet_resources = rl.load_texture(b"assets/resources.png")


    def tick(self):
        pass

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
        rl.unload_texture(self.img_sprite_sheet)

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

        self.map[building_selected.y][building_selected.x] = building_selected
        for i in range(building_selected.height):
            for j in range(building_selected.width):
                
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
        return True