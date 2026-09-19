import pyray as rl

resources_info = {
    "people": (0),
    "water": (1),
    "food": (2),
    "energy": (3),
    "ore": (4),
    "iron": (5),
    "mushroom": (6),
    "coal": (7),
    "sewage": (8),
    "steel": (9),
    "gold": (10), 
    "silicon": (11),
    "hydrogen": (12), 
    "uranium": (13), 
    "diamond": (14), 
    "nuclear": (15), 
    "chip": (16), 
    "rocket": (17), 
    }

resources_flux = set(["energy", "people"])

class Resources:

    def get_resources_names():
        names = list(resources_info.keys())
        names.remove("ground")  # Remove "ground" da lista, pois não é uma construção que o jogador pode construir
        return names

    def __init__(self, id):
        self.id = id
        self.y_sprite_sheet, self.x_sprite_sheet, = resources_info[id]

    