import pyray as rl
import math
from sidebar_menu import SidebarMenu
from resource_bar import ResourceBar

class HUD:
    def __init__(self, game_manager, resources):
        self.game_manager = game_manager
        self.resources = resources
        self.sidebar = SidebarMenu(self)
        self.resource_bar = ResourceBar(self)
        self.selection_action = None
        
        # Variáveis novas de estado de ferramenta
        self.current_tool = None # Pode ser "move" ou "destroy"
        self.is_moving = False # Para não cobrar custo quando soltar

    def tick(self):
        self.sidebar.update()
        self.resource_bar.update()
        
        # Se ESC, limpa tudo
        if rl.is_key_pressed(rl.KEY_ESCAPE):
            self.selection_action = None
            self.current_tool = None
            self.is_moving = False

        # Verifica cliques e ações do mouse fora da sidebar
        if rl.get_mouse_x() < rl.get_screen_width() - self.sidebar.width:
            cam = self.game_manager.camera
            exact_x = (rl.get_mouse_x() / (cam.escala * cam.zoom)) - cam.pos.x
            exact_y = (rl.get_mouse_y() / (cam.escala * cam.zoom)) - cam.pos.y
            grid_x = math.floor(exact_x)
            grid_y = math.floor(exact_y)

            # Tem uma construção na mão para colocar (Build ou soltando o Move)
            if self.selection_action:
                self.selection_action.x = grid_x
                self.selection_action.y = grid_y

                if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
                    # Passa o is_moving pra saber se cobra ou não (free=True)
                    if self.game_manager.world.place_building(self.selection_action, free=self.is_moving):
                        self.selection_action = None
                        self.is_moving = False # Finalizou o move

            # Não tem construção na mão, mas clicou com a ferramenta de Mover ou Destruir selecionada
            elif rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
                if 0 <= grid_x < self.game_manager.world.width and 0 <= grid_y < self.game_manager.world.height:
                    if self.current_tool == "destroy":
                        self.game_manager.world.destroy_building(grid_x, grid_y)
                    
                    elif self.current_tool == "move":
                        picked = self.game_manager.world.pick_up_building(grid_x, grid_y)
                        if picked:
                            self.selection_action = picked
                            self.is_moving = True

    def render(self):
        self.sidebar.render()
        self.resource_bar.render()
        
        # Feedback visual para as ferramentas
        if not self.selection_action and self.current_tool in ["destroy", "move"]:
            if rl.get_mouse_x() < rl.get_screen_width() - self.sidebar.width:
                cam = self.game_manager.camera
                exact_x = (rl.get_mouse_x() / (cam.escala * cam.zoom)) - cam.pos.x
                exact_y = (rl.get_mouse_y() / (cam.escala * cam.zoom)) - cam.pos.y
                
                # Se estiver no mapa, desenha um bloco colorido vermelho (destroy) ou azul (move) no bloco apontado
                if 0 <= math.floor(exact_x) < self.game_manager.world.width and 0 <= math.floor(exact_y) < self.game_manager.world.height:
                    color = rl.RED if self.current_tool == "destroy" else rl.BLUE
                    
                    parent = self.game_manager.world.get_parent_building(math.floor(exact_x), math.floor(exact_y))
                    if parent:
                        # Pinta a construção inteira alvo
                        cam.draw_rect(rl.Rectangle(parent.x, parent.y, parent.width, parent.height), rl.fade(color, 0.5))

        if self.selection_action:
            self.game_manager.camera.draw_building(
                self.game_manager.world.img_sprite_sheet_buildings, 
                self.selection_action, 
                highlight=True
            )