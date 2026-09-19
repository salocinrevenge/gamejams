import pyray as rl

from infos import resources




class Resources:

    def get_resources_names():
        names = list(resources.keys())
        names.remove("ground")  # Remove "ground" da lista, pois não é uma construção que o jogador pode construir
        return names

    def __init__(self, id):
        self.id = id
        self.y_sprite_sheet, self.x_sprite_sheet, = resources[id]

    