

from raylib import rl


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

    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        

        self.y_sprite_sheet, self.x_sprite_sheet, self.width, self.height = self.info[id]

    