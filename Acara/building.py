import pyray as rl


class Building:

    info = {
        "ground": (0, 0, 1, 1),
        "pump": (1, 0, 1, 1),
        "farm": (2, 0, 2, 1),
        "treatment": (3, 0, 3, 2),
        "tent": (5, 0, 1, 1),
        "solar": (6, 0, 1, 1),
        "miner": (7, 0, 1, 1),
        "bin": (8, 0, 1, 1),
        "tank": (9, 0, 1, 1),
        "resources": (10 , 0, 3, 3),
        "sewage": (13 , 0, 1, 1),
    }

    def get_buildings_names():
        names = list(Building.info.keys())
        names.remove("ground")  # Remove "ground" da lista, pois não é uma construção que o jogador pode construir
        return names

    def __init__(self, id, x, y, parent=None, shift_sprite_sheet=rl.Vector2(0, 0)):
        self.id = id
        self.x = x
        self.y = y
        self.parent = parent
        
        self.y_sprite_sheet, self.x_sprite_sheet, self.width, self.height = self.info[id]
        self.x_sprite_sheet += shift_sprite_sheet.x
        self.y_sprite_sheet += shift_sprite_sheet.y

    