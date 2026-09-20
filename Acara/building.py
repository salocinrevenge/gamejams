import pyray as rl

from infos import buildings

class Building:
    def get_buildings_names():
        names = list(buildings.keys())
        names.remove("ground")  # Remove "ground" da lista, pois não é uma construção que o jogador pode construir
        return names

    def __init__(self, id, x, y, parent=None, shift_sprite_sheet=rl.Vector2(0, 0)):
        self.id = id
        self.x = x
        self.y = y
        self.parent = parent
        
        self.info = buildings
        self.y_sprite_sheet, self.x_sprite_sheet, self.width, self.height = self.info[id]["sprite_info"]
        self.x_sprite_sheet += shift_sprite_sheet.x
        self.y_sprite_sheet += shift_sprite_sheet.y
        
        self.timer = 0  # Timer individual para a construção
        self.active_upgrade = None 
        self.is_working = False
        self.missing_resources = []

    