import pyray as rl
import math
from sidebar_menu import SidebarMenu
from resource_bar import ResourceBar

class HUD:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.sidebar = SidebarMenu(self)  # Instancia o menu lateral modularizado
        self.resource_bar = ResourceBar(self)
        self.selection_action = None

        self.resources = {
            "people": 15,
            "water ": 100,
            "food ": 50,
            "energy ": 0,
            "ore ": 10,
            "iron ": 0,
            "mushroom ": 5,
            "coal": 0,
            "sewage": 0,
            "steel": 0,
            "gold": 2,
            "hydrogen": 0,
            "uranium": 0,
            "diamond": 1,
            "nuclear": 0,
            "chip": 0,
            "rocket ": 0,
        }

    def tick(self):
        # Atualiza o menu lateral (scroll, etc.)
        self.sidebar.update()
        self.resource_bar.update()
        
        # Atualiza a posição do objeto selecionado seguindo o mouse com snap na grade
        if self.selection_action:
            mouse_pos = rl.get_mouse_position()
            cam = self.game_manager.camera
            
            exact_x = (mouse_pos.x / (cam.escala * cam.zoom)) - cam.pos.x
            exact_y = (mouse_pos.y / (cam.escala * cam.zoom)) - cam.pos.y
            
            self.selection_action.x = math.floor(exact_x)
            self.selection_action.y = math.floor(exact_y)

            if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
                print(f"Construção {self.selection_action.id} colocada em ({self.selection_action.x}, {self.selection_action.y})")
                if self.game_manager.world.place_building(self.selection_action):
                    self.selection_action = None

    def render(self):
        # Renderiza o menu lateral modularizado
        self.sidebar.render()
        self.resource_bar.render()
        
        # Se houver uma construção selecionada na mão, desenha ela seguindo o mouse
        if self.selection_action:
            self.game_manager.camera.draw_building(
                self.game_manager.world.img_sprite_sheet_buildings, 
                self.selection_action, 
                highlight=True
            )